#!/usr/bin/env python
import argparse
import sys
import time

import logging
log = logging.getLogger()

from display.worlds.split import TwoLayerWorld
from display.sprites.atmosphere import Sky, Stars, Ground, Rain, CloudCover
from display.sprites.atmosphere import ExpandingSplotches
from display.sprites.solid import SingleColor
from display.sprites.solid import SequenceColor
from display.sprites.ombre import OmbreColor, OuterInnterOmbre

from display.dynamics.ombre import OmbreMergeToDynamic, OmbreMergeFromDynamic
from display import Pixel

from agent.frame import RedisFrameAgent

from core.profile import start_profiler, stop_profiler

import uuid
import signal


def world_callback(world):
    return False

PIXELS = 447
OUTER_PIXELS = 235

if __name__ == "__main__":
    log.setLevel(logging.INFO)
    logging.basicConfig(format="%(thread)d:%(asctime)s:%(levelname)s:%(module)s :: %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument('--virtual', action="store_true", dest="virtual", default=False,
                        help='Use pygame display')
    parser.add_argument('--led', action="store_true", dest="led", default=False,
                        help='Use led display')

    parser.add_argument('--fps', action="store_true", dest="fps", default=False,
                        help='Show FPS')
    parser.add_argument('--profiler', action="store_true", dest="profiler", default=False,
                        help='Run timing profiler')

    parser.add_argument('--pixels', default="447",
                        help='How many pixels in the display')

    parser.add_argument('--outer-pixels', default="235",
                        help='Number of pixels in the outer layer')

    parser.add_argument('--redis', default=None,
                        help="Subscribe to a redis server on the localhost at default ports with supplied pubsub key")

    parser.add_argument('scene', default="o_grass,o_clouds,i_night,i_stars", nargs='?',
                        help='Which scenes to composite.  Choices include: sky, grass, dirt, night, rain, clouds, stars')


    args = parser.parse_args(sys.argv[1:])

    enable_threading = True
    if args.virtual:
        enable_threading = False

    if args.pixels:
        PIXELS = int(args.pixels)
    if args.outer_pixels:
        OUTER_PIXELS = int(args.outer_pixels)

    scene = TwoLayerWorld(OUTER_PIXELS, PIXELS - OUTER_PIXELS, print_fps=args.fps, enable_threading=enable_threading)

    if args.virtual:
        from display.renderers.shape import PyGameSplitShape
        scene.add_renderer( PyGameSplitShape(OUTER_PIXELS) )
    if args.led:
        from display.renderers.led import NeoPixelRenderer
        scene.add_renderer( NeoPixelRenderer() )

    for item in args.scene.split(","):
        target = item.split("_")[-1]
        layer_indicator = item.split("_")[0]

        pixel_count = OUTER_PIXELS
        layer = TwoLayerWorld.OUTER_TRACK
        if layer_indicator == "i":
            pixel_count = PIXELS - OUTER_PIXELS
            layer = TwoLayerWorld.INNER_TRACK

        if "single" == target:
            components = item.split("_")
            color = Pixel( int(components[1]),
                           int(components[2]),
                           int(components[3]) )

            # scene.add_sprite( SingleColor( color ), layer )
            scene.add_sprite( SequenceColor( [color] ), layer )


        if "ombre" in target:
            components = item.split("_")
            from_color = Pixel( int(components[1]),
                                int(components[2]),
                                int(components[3]) )

            to_color = Pixel( int(components[4]),
                              int(components[5]),
                              int(components[6]) )

            ombre_cls = OmbreColor
            if "ombre-oi" == target:
                ombre_cls = OuterInnterOmbre

            sprite = ombre_cls(from_color, to_color)
            # sprite.add_dynamic( OmbreMergeToDynamic(merge_time_ms=5*1000) )
            sprite.add_dynamic( OmbreMergeFromDynamic(merge_time_ms=5*1000) )
            scene.add_sprite( sprite, layer )

        if "sequence" == target:
            scene.add_sprite( SequenceColor([
                Pixel(246,215,176),
                Pixel(118,182,196),
                Pixel(0, 189, 254),
                Pixel(0, 189, 254),
                Pixel(255, 204, 51),
                Pixel(0, 189, 254),
                Pixel(118,182,196),
                Pixel(246,215,176)
                ]), layer)

        if "sky" == target:
            scene.add_sprite( Sky(clouds=2, world_size=pixel_count), layer )

        if "grass" == target:
            scene.add_sprite( Ground(ground_color=Ground.MEADOW_COLOR, brightness_variance=0.10), layer )

        if "dirt" == target:
            scene.add_sprite( Ground(ground_color=Ground.DIRT_COLOR, brightness_variance=0.05), layer )

        if "night" == target:
            scene.add_sprite( Ground(ground_color=Ground.NIGHT_COLOR, brightness_variance=0.0), layer )

        if "rain" == target:
            scene.add_sprite( Rain(max_drops=10, drop_rate=.1, world_size=pixel_count), layer )

        if "clouds" == target:
            scene.add_sprite( CloudCover(clouds=2, world_size=pixel_count, cloud_min_radius=2, cloud_max_radius=int(pixel_count*0.2)), layer )

        if "stars" == target:
            scene.add_sprite( Stars(stars=5, world_size=pixel_count), layer )

        if "expand" == target:
            scene.add_sprite( ExpandingSplotches(), layer )


    if args.redis:
        agent = RedisFrameAgent(str(uuid.uuid4()), scene, args.redis)
        agent.run()

    def signal_handler(signal, frame):
        print('\nStopping world run loop\n')
        scene.stop()
        if agent:
            agent.stop()

    signal.signal(signal.SIGINT, signal_handler)

    #track activity if option is set
    profiler = start_profiler() if args.profiler else None

    scene.run( world_callback )
    while scene.run_enable:
        time.sleep(1)

    #if we're tracking activity, stop
    if profiler:
        stop_profiler(profiler)
