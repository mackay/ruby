
import pygame
from pygame.locals import DOUBLEBUF

from display import Renderer


class PyGameRenderer(Renderer):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super(PyGameRenderer, self).__init__()

    def setup(self, pixel_count, world):
        super(PyGameRenderer, self).setup(pixel_count, world)
        pygame.init()

        self.window = (self.width, self.height)
        self.flags = DOUBLEBUF

        self.screen = pygame.display.set_mode(self.window, self.flags)
        self.background = pygame.Surface(self.window)

        #keep a reference to the world - pygame has feeback to process
        self.world = world

    def render_buffer(self, pixel_buffer):
        super(PyGameRenderer, self).render_buffer(pixel_buffer)

        self._process_pygame_events()

        if self._is_buffer_changed(pixel_buffer):
            self._render_buffer_internal(pixel_buffer)

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def _render_buffer_internal(self, pixel_buffer):
        return

    def _to_color(self, pixel):
        return (pixel.r, pixel.g, pixel.b, pixel.a)

    def _process_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_enable = False


class PyGameLinearRenderer(PyGameRenderer):

    def __init__(self, width=1200, height=40):
        self.target_height = height
        self.target_width = width
        super(PyGameLinearRenderer, self).__init__(width, height)

    def setup(self, pixel_count, world):
        self.height = self.target_height
        self.width = ( self.target_width / pixel_count ) * pixel_count

        super(PyGameLinearRenderer, self).setup(pixel_count, world)

    def _render_buffer_internal(self, pixel_buffer):
        pixel_width = self.width / len(pixel_buffer)
        pixel_height = self.height

        for idx, pixel in enumerate(pixel_buffer):
            pygame.draw.rect( self.background,
                              self._to_color(pixel),
                              ( idx*pixel_width, 0,
                                pixel_width, pixel_height) )
