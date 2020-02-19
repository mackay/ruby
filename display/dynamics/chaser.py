from display import Dynamic


class ChaserPosition(Dynamic):
    def __init__(self, speed_ms=100, mask_start_position=0):
        self.speed_ms = speed_ms
        self.position = mask_start_position

        self.accumulated_time_ms = 0
        super(ChaserPosition, self).__init__()

    def act_on(self, sprite, world, elapsed_time_ms):
        super(ChaserPosition, self).act_on(sprite, world, elapsed_time_ms)

        self.accumulated_time_ms += elapsed_time_ms
        pixels = world.pixels_for_sprite(sprite)

        while self.accumulated_time_ms > self.speed_ms:
            self.accumulated_time_ms -= self.speed_ms
            self._iterate_chaser(sprite, world, pixels)

    def _iterate_chaser(self, sprite, world, pixels):
        self.position += 1
        sprite.position = self.position


class ChaserPositionReverse(ChaserPosition):
    def _iterate_chaser(self, sprite, world, pixels):
        super(ChaserPositionReverse, self)._iterate_chaser(sprite, world, pixels)
        sprite.position = len(pixels) - self.position
