import math
from display import Dynamic
from display.gradient import pixel_gradient


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
        pixel_choices = pixel_gradient( sprite.state["original_from"],
                                        sprite.state["original_to"],
                                        pixel_len,
                                        to_shoulder=sprite.to_shoulder)
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



class OmbreShiftToDynamic(OmbreMergeToDynamic):

    def _set_color(self, sprite, elapsed_percent, colors):

        pixel_choice = min( int(math.ceil(len(colors) * elapsed_percent)),
                            len(colors) - 1 )
        sprite.from_color = colors[ pixel_choice ]
