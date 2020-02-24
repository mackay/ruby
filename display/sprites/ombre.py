from display import DynamicSprite
from display.gradient import pixel_gradient


class OmbreColor(DynamicSprite):
    def __init__(self, from_color, to_color, to_shoulder=0, pixel_block_size=4):
        super(OmbreColor, self).__init__()
        self.from_color = from_color
        self.to_color = to_color
        self.to_shoulder = 0
        self.pixel_block_size = pixel_block_size

    def _pixel_gradient(self, n_pixels):
        return pixel_gradient(self.from_color,
                              self.to_color,
                              n_pixels,
                              to_shoulder=self.to_shoulder)

    def _do_render(self, pixel_buffer):
        pixel_buffer_len = len(pixel_buffer)
        colors = self._pixel_gradient(pixel_buffer_len)

        colors_max_index = len(colors) - 1

        previous_pixel = None
        for i in range(0, pixel_buffer_len):
            if i and previous_pixel and int(i) % self.pixel_block_size:
                pixel_buffer[i].set_color_n( previous_pixel.r_n,
                                             previous_pixel.g_n,
                                             previous_pixel.b_n,
                                             previous_pixel.a_n )
            else:
                pixel_buffer[i].blend( colors[min(i, colors_max_index)] )
                previous_pixel = pixel_buffer[i]

        super(OmbreColor, self)._do_render(pixel_buffer)


class OuterInnterOmbre(OmbreColor):

    def _pixel_gradient(self, n_pixels):
        return pixel_gradient(self.from_color,
                              self.to_color,
                              n_pixels,
                              to_shoulder=self.to_shoulder,
                              is_centered=True)