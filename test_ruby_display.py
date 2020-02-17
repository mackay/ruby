import pygame
from pygame.locals import DOUBLEBUF
import math
import time


def normalize_legs(source):
    segment_total = 0.0
    for segment in source:
        segment_total += float(segment[-1])

    for segment in source:
        segment[-1] = float(segment[-1]) / segment_total

    return source

def draw_shape(surface, pixels, edges, margin, width, height):
    pixel_start_index = 0
    for edge in edges:
        pixel_end_index = pixel_start_index + int(math.floor(len(pixels) * edge[-1]))
        start_xy = ( edge[0][0] * ( width - 2 * margin ) + margin, edge[0][1] * ( height - 2 * margin ) + margin )
        end_xy = ( edge[1][0] * ( width - 2 * margin ) + margin, edge[1][1] * ( height - 2 * margin ) + margin )

        for idx, point in enumerate(points_along_line( start_xy, end_xy, pixel_end_index - pixel_start_index )):
            pygame.draw.circle(surface, pixels[pixel_start_index + idx], ( int(point[0]), int(point[1]) ), 3 )

def points_along_line( start_xy, end_xy, point_count ):
    x_run = ( end_xy[0] - start_xy[0] ) / point_count
    y_run = ( end_xy[1] - start_xy[1] ) / point_count

    x_pos = start_xy[0]
    y_pos = start_xy[1]

    for i in range(point_count):
        yield ( x_pos, y_pos )
        x_pos += x_run
        y_pos += y_run

def draw_ruby():
    height = 300
    width = 400
    margins = 20

    pygame.init()

    window = (width, height)
    flags = DOUBLEBUF
    screen = pygame.display.set_mode(window, flags)
    background = pygame.Surface(window)

    outer_pixels = [ (  0, 255, 255, 255) ] * 400
    inner_pixels = [ (255,   0, 255, 255) ] * 300

    #(x ratio, y ratio) to ( x ratio, y ratio )
    ruby_legs = normalize_legs([
        [ (0.33, 1.0), (0.0,  0.4), 6 ],
        [ (0.0,  0.4), (0.2,  0.0), 3 ],
        [ (0.2,  0.0), (0.8,  0.0), 6 ],
        [ (0.8,  0.0), (1.0,  0.4), 3 ],
        [ (1.0,  0.4), (0.66, 1.0), 6 ]
    ])

    draw_shape(background, outer_pixels, ruby_legs, margins, width, height)
    draw_shape(background, inner_pixels, ruby_legs, margins*2, width, height)

    screen.blit(background, (0, 0))
    pygame.display.flip()
    pygame.display.update()


while True:
    draw_ruby()
    time.sleep(40. / 1000.)
