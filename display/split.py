from display.sequence import SequenceWorld


class TwoLayerWorld(SequenceWorld):
    OUTER_TRACK = "outer"
    INNER_TRACK = "inner"

    def __init__(self, outer_pixel_count, inner_pixel_count, print_fps=False, timing_ms_per_update=33.3, enable_threading=True):
        self.outer_pixel_count = outer_pixel_count
        self.inner_pixel_count = inner_pixel_count
        self.inner_sprite_id = [ ]

        super(TwoLayerWorld, self).__init__(outer_pixel_count + inner_pixel_count, print_fps=print_fps, timing_ms_per_update=timing_ms_per_update, enable_threading=enable_threading)

    def pixels_for_sprite(self, sprite):
        if sprite.id in self.inner_sprite_id:
            return self.pixels[self.outer_pixel_count:]

        return self.pixels[:self.outer_pixel_count]

    def clear_sprites(self):
        self.inner_sprite_id = [ ]
        return super(TwoLayerWorld, self).clear_sprites()

    def add_sprite(self, sprite, layer):
        if layer == self.INNER_TRACK:
            self.inner_sprite_id.append(sprite.id)
        return super(TwoLayerWorld, self).add_sprite(sprite)

    def remove_sprite(self, sprite, recurse=True):
        self.inner_sprite_id = [ id for id in self.inner_sprite_id if id != sprite.id ]
        return super(TwoLayerWorld, self).remove_sprite(sprite, recurse=recurse)
