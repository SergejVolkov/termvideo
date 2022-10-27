import numpy as np

from .base_single import base_single_cmap


class base_lagtrain_cmap(base_single_cmap):
    def __init__(self, back: int = 178, eps: tuple = (11, 7), **kwargs):
        super().__init__(**kwargs)
        self.back = back
        self.eps = eps

    def map(self, img: np.ndarray) -> np.ndarray:
        grayscale = img.mean(axis=-1)
        out = np.full_like(grayscale, self.gray, dtype=np.uint8)
        out[self.back + self.eps[1] < grayscale] = self.white
        out[grayscale < self.back - self.eps[0]] = self.black
        return out
