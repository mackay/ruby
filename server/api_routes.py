from bottle import hook
from bottle import abort
from bottle import request, post, delete, get

from core.apiutil import require_fields, serialize_json, get_configuration
from core.models import database
from core.system import SystemBase

from display.worlds.split import TwoLayerWorld

import pickle
import redis
import json

import logging
log = logging.getLogger()


networks = None


def load_networks():
    networks = [ ]

    config = get_configuration()
    for network_file_source in config["networks"]:
        with open(network_file_source, 'rb') as network:
            networks.append( pickle.load(network) )

    return networks


@hook('before_request')
def before_request():
    database.connect()


@hook('after_request')
def after_request():
    database.close()


# System configuration
@post('/option', is_api=True)
@require_fields(["key", "value"])
@serialize_json()
def post_option():
    body = request.json
    return SystemBase().set_option(body["key"], body["value"])


@get('/option', is_api=True)
@serialize_json()
def get_option():
    return SystemBase().get_options()


# sequences
@get('/sequence', is_api=True)
@serialize_json()
def get_sequences():
    pass


@post('/sequence', is_api=True)
@serialize_json()
def create_sequence():
    pass


@post('/presentation/sequence', is_api=True)
@serialize_json()
def present_sequence():
    pass


@post('/presentation/outer', is_api=True)
@serialize_json()
def present_outer():
    _publish_color( request.json["pixels"], TwoLayerWorld.OUTER_TRACK )
    # colors = request.json["pixels"]
    # sequence = json.dumps(_sequence_from_colors(colors, TwoLayerWorld.OUTER_TRACK))

    # r = redis.Redis(host="localhost", port=6379, db=0)
    # r.publish("ruby", sequence)


@post('/presentation/inner', is_api=True)
@serialize_json()
def present_inner():
    _publish_color( request.json["pixels"], TwoLayerWorld.INNER_TRACK )
    # colors = request.json["pixels"]
    # sequence = json.dumps(_sequence_from_colors(colors, TwoLayerWorld.INNER_TRACK))

    # r = redis.Redis(host="localhost", port=6379, db=0)
    # r.publish("ruby", sequence)

def _publish_color(colors, layer):
    if len(colors) == 1:
        colors = [ colors[0], colors[0] ]

    sequence = json.dumps(_sequence_from_colors(colors, layer))
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.publish("ruby", sequence)


def _sequence_from_colors(hex_colors, layer):
    pixels = [ ]
    for color in hex_colors:
        if color[0] != "#":
            color = "#" + color

        pixels.append( "Pixel|" + color )

    return {
        "frames": [
            {
                "duration_ms": 1,
                "sprites": [
                    {
                        "class_path": "display.sprites.ombre.OuterInnterOmbre",
                        "args": pixels,
                        "layer": layer
                    }
                ]
            }
        ]
    }
