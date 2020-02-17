import math
import pygame
from display.renderers.virtual import PyGameRenderer


class PyGameSplitShape(PyGameRenderer):
    #(x ratio, y ratio) to ( x ratio, y ratio )
    RUBY_EDGES = [
        [ (0.33, 1.0), (0.0,  0.4), 6 ],
        [ (0.0,  0.4), (0.2,  0.0), 3 ],
        [ (0.2,  0.0), (0.8,  0.0), 6 ],
        [ (0.8,  0.0), (1.0,  0.4), 3 ],
        [ (1.0,  0.4), (0.66, 1.0), 6 ]
    ]

    def __init__(self, outer_pixel_count, width=400, height=300, margins=20, edges=None):
        super(PyGameSplitShape, self).__init__(width, height)

        self.margins = margins
        self.outer_pixel_count = outer_pixel_count

        edges = edges or PyGameSplitShape.RUBY_EDGES
        self.edges = self._normalize_legs(edges)

    def _normalize_legs(self, source):
        segment_total = 0.0
        for segment in source:
            segment_total += float(segment[-1])

        for segment in source:
            segment[-1] = float(segment[-1]) / segment_total

        return source

    def _draw_shape(self, pixels, margin=None):
        width = self.width
        height = self.height
        margin = margin or self.margins

        pixel_start_index = 0
        for edge in self.edges:
            edge_pixel_length = int(math.floor(len(pixels) * edge[-1]))

            pixel_end_index = pixel_start_index + edge_pixel_length
            start_xy = ( edge[0][0] * ( width - 2 * margin ) + margin, edge[0][1] * ( height - 2 * margin ) + margin )
            end_xy = ( edge[1][0] * ( width - 2 * margin ) + margin, edge[1][1] * ( height - 2 * margin ) + margin )

            for idx, point in enumerate(self._points_along_line( start_xy, end_xy, pixel_end_index - pixel_start_index )):
                pygame.draw.circle(self.background, self._to_color(pixels[pixel_start_index + idx]), ( int(point[0]), int(point[1]) ), 3 )

            pixel_start_index += edge_pixel_length

    def _points_along_line(self, start_xy, end_xy, point_count ):
        x_run = ( end_xy[0] - start_xy[0] ) / point_count
        y_run = ( end_xy[1] - start_xy[1] ) / point_count

        x_pos = start_xy[0]
        y_pos = start_xy[1]

        for i in range(point_count):
            yield ( x_pos, y_pos )
            x_pos += x_run
            y_pos += y_run

    def _render_buffer_internal(self, pixel_buffer):
        self._draw_shape(pixel_buffer[:self.outer_pixel_count], margin=self.margins)
        self._draw_shape(pixel_buffer[self.outer_pixel_count:], margin=self.margins*2)
