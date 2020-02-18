from display import DynamicSprite
from display.gradient import pixel_gradient


class OmbreColor(DynamicSprite):
    def __init__(self, from_color, to_color, to_shoulder=0):
        super(OmbreColor, self).__init__()
        self.from_color = from_color
        self.to_color = to_color
        self.to_shoulder = 0

    def _pixel_gradient(self, n_pixels):
        return pixel_gradient(self.from_color,
                              self.to_color,
                              n_pixels,
                              to_shoulder=self.to_shoulder)

    def render_to(self, pixel_buffer):
        pixel_buffer_len = len(pixel_buffer)
        colors = self._pixel_gradient(pixel_buffer_len)

        for i in range(0, pixel_buffer_len):
            pixel_buffer[i].blend( colors[i] )

        super(OmbreColor, self).render_to(pixel_buffer)


class OuterInnterOmbre(OmbreColor):

    def _pixel_gradient(self, n_pixels):
        return pixel_gradient(self.from_color,
                              self.to_color,
                              n_pixels,
                              to_shoulder=self.to_shoulder,
                              is_centered=True)