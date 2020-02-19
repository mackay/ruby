import math
from display import DynamicSprite


class SingleColor(DynamicSprite):
    def __init__(self, color):
        super(SingleColor, self).__init__()
        self.color = color

    def _do_render(self, pixel_buffer):
        for i in range(0, len(pixel_buffer)):
            pixel_buffer[i].blend( self.color )

        super(SingleColor, self)._do_render(pixel_buffer)


class SequenceColor(DynamicSprite):
    def __init__(self, colors):
        super(SequenceColor, self).__init__()
        self.colors = colors

    def _do_render(self, pixel_buffer):
        pixels_per_color = int(math.ceil(len(pixel_buffer) / len(self.colors)))
        for i in range(0, len(pixel_buffer)):
            color_index = int(math.floor( i / pixels_per_color ))
            color_index = min( color_index, len(self.colors) - 1 )

            pixel_buffer[i].blend( self.colors[color_index] )

        super(SequenceColor, self)._do_render(pixel_buffer)
