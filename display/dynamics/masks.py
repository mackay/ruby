from display.dynamics.chaser import ChaserPosition


class ChaserMask(ChaserPosition):
    def _iterate_chaser(self, sprite, world, pixels):
        super(ChaserMask, self)._iterate_chaser(sprite, world, pixels)
        sprite.mask = self._build_mask(pixels)

    def _build_mask(self, for_pixels):
        mask = [ 0 ] * len(for_pixels)
        for i in range(self.position):
            mask[i] = 1
        return mask


class DualChaserMask(ChaserMask):

    def _build_mask(self, for_pixels):
        self.position = min(self.position, len(for_pixels) - 1)

        mask = [ 0 ] * len(for_pixels)
        for i in range(self.position):
            mask[i] = 1
            mask[ len(mask) - i - 1 ] = 1
        return mask
