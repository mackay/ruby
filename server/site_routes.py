from bottle import static_file, route
from bottle import view

from core.models import Sequence

import logging
log = logging.getLogger()


@route('/')
@view('home')
def static_index():
    template_data = {
        "sequences": [ s for s in Sequence.select() ]
    }
    return template_data


@route('/<filename:path>')
def all_static(filename):
    return static_file(filename, root='./server/static')
