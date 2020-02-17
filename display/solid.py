import math

from display import Pixel, DynamicSprite
from display import Dynamic
from display.gradient import RGB_to_hex, hex_to_RGB, bezier_gradient

class SingleColor(DynamicSprite):
    def __init__(self, color):
        super(SingleColor, self).__init__()
        self.color = color

    def render_to(self, pixel_buffer):
        for i in range(0, len(pixel_buffer)):
            pixel_buffer[i].blend( self.color )

        super(SingleColor, self).render_to(pixel_buffer)


class OmbreColor(DynamicSprite):
    def __init__(self, from_color, to_color, to_shoulder=0):
        super(OmbreColor, self).__init__()
        self.from_color = from_color
        self.to_color = to_color
        self.to_shoulder = 0

    def _pixel_gradient(self, n_pixels):
        from_hex = RGB_to_hex([self.from_color.r, self.from_color.g, self.from_color.b])
        to_hex = RGB_to_hex([self.to_color.r, self.to_color.g, self.to_color.b])

        gradient_length = n_pixels - self.to_shoulder

        rgb_colors = [ ]
        if gradient_length > 2:
            rgb_colors = [ hex_to_RGB(c) for c in bezier_gradient([from_hex, to_hex], gradient_length)["hex"] ]

        return [ Pixel(c[0], c[1], c[2]) for c in rgb_colors ] + [ self.to_color ] * self.to_shoulder

    def render_to(self, pixel_buffer):
        pixel_buffer_len = len(pixel_buffer)
        colors = self._pixel_gradient(pixel_buffer_len)

        for i in range(0, pixel_buffer_len):
            pixel_buffer[i].blend( colors[i] )

        super(OmbreColor, self).render_to(pixel_buffer)


class OuterInnterOmbre(OmbreColor):

    def _pixel_gradient(self, n_pixels):
        from_hex = RGB_to_hex([self.from_color.r, self.from_color.g, self.from_color.b])
        to_hex = RGB_to_hex([self.to_color.r, self.to_color.g, self.to_color.b])

        gradient_length = n_pixels - self.to_shoulder
        rgb_colors = [ ]
        if gradient_length > 2:
            rgb_colors = [ hex_to_RGB(c) for c in bezier_gradient([from_hex, to_hex], int(math.ceil(gradient_length / 2)))["hex"] ]

        gradient = [ Pixel(c[0], c[1], c[2]) for c in rgb_colors ] + [ self.to_color ] * int(math.ceil(self.to_shoulder / 2))

        for i in range( len(gradient) - 1, -1, -1) :
            gradient.append(gradient[i])

        return gradient


class OmbreShoulderDynamic(Dynamic):
    def __init__(self, merge_time_ms=1000*10):
        super(OmbreShoulderDynamic, self).__init__()
        self.merge_time_ms = merge_time_ms
        self.elapsed_time_ms = 0

    def act_on(self, sprite, world, elapsed_time):
        super(OmbreShoulderDynamic, self).act_on(sprite, world, elapsed_time)

        self.elapsed_time_ms += elapsed_time

        pixel_size = len(world.pixels_for_sprite(sprite))
        elapsed_percent = float(self.elapsed_time_ms) / float(self.merge_time_ms)
        sprite.to_shoulder = pixel_size * elapsed_percent


class OmbreMergeToDynamic(Dynamic):
    def __init__(self, merge_time_ms=1000*10):
        super(OmbreMergeToDynamic, self).__init__()
        self.merge_time_ms = merge_time_ms
        self.elapsed_time_ms = 0

    def act_on(self, sprite, world, elapsed_time):
        super(OmbreMergeToDynamic, self).act_on(sprite, world, elapsed_time)

        if self.elapsed_time_ms < self.merge_time_ms:
            self.elapsed_time_ms += elapsed_time
        else:
            self.elapsed_time_ms = self.merge_time_ms
        elapsed_percent = float(self.elapsed_time_ms) / float(self.merge_time_ms)

        if "original_from" not in sprite.state:
            sprite.state["original_from"] = sprite.from_color
            sprite.state["original_to"] = sprite.to_color

        pixel_len = len(world.pixels_for_sprite(sprite))
        pixel_choices = OmbreColor( sprite.state["original_from"],
                                    sprite.state["original_to"],
                                    sprite.to_shoulder)._pixel_gradient(pixel_len)
        self._set_color(sprite, elapsed_percent, pixel_choices)

    def _set_color(self, sprite, elapsed_percent, colors):
        pixel_choice = min( int(math.ceil(len(colors) * elapsed_percent)),
                            len(colors) - 1 )
        sprite.from_color = colors[ pixel_choice ]


class OmbreMergeFromDynamic(OmbreMergeToDynamic):

    def _set_color(self, sprite, elapsed_percent, colors):
        pixel_choice = min( int(math.ceil(len(colors) * elapsed_percent)),
                            len(colors) - 1 )
        pixel_choice = min( len(colors) - 1, len(colors) - pixel_choice )
        sprite.to_color = colors[ pixel_choice ]
