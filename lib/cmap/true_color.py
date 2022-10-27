import numpy as np

from .. import color
from .base_single import base_single_cmap


class common(base_single_cmap):
    #: True color palette.
    palette = color.true_color.palette

    def map(self, img: np.ndarray) -> np.ndarray:
        img = img.astype(int)
        out = img[..., 0] * 256 ** 2 + img[..., 1] * 256 + img[..., 2]
        return out


class fast(common):
    def map(self, img: np.ndarray) -> np.ndarray:
        img = (img // 16 * 16).astype(int)
        out = img[..., 0] * 256 ** 2 + img[..., 1] * 256 + img[..., 2]
        return out
