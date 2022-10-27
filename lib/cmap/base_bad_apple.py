import numpy as np

from .base_single import base_single_cmap


class base_bad_apple_cmap(base_single_cmap):
    def map(self, img: np.ndarray) -> np.ndarray:
        grayscale = img.mean(axis=-1)
        out = (grayscale > 255 / 2).astype(np.uint8) * self.white
        return out
