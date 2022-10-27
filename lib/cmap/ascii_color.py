import numpy as np
from typing import Tuple

from .. import color
from ..color.terminal import hpalette, hrgb_norm
from .base_multi import base_multi_cmap


class common(base_multi_cmap):
    #: Combined palette.
    palette = [hpalette, color.ascii.palette]

    def __init__(self, eps: float = 1e-3, **kwargs):
        super().__init__(**kwargs)
        self.eps = eps

    def map(self, img: np.ndarray) -> Tuple[np.ndarray, ...]:
        shifted = img + self.eps
        normalized = shifted / np.max(shifted, axis=-1, keepdims=True)
        normalized = np.expand_dims(normalized, -2)
        color_index = np.argmin(
            np.abs(normalized - np.expand_dims(hrgb_norm, (0, 1))).mean(axis=-1),
            axis=-1
        )

        grayscale = img.mean(axis=-1) + 0.5

        return color_index.astype(np.uint8), grayscale.astype(np.uint8)


# class unicode(ascii):
#     #: Combined palette.
#     palette = [hpalette, color.unicode.palette]


# common = ascii
