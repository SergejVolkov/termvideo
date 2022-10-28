import numpy as np
from typing import Tuple

from .. import color
from .base_multi import base_multi_cmap


class common(base_multi_cmap):
    #: Combined palette.
    palette = [color.true_color.fore_palette, color.ascii.palette]

    #: Number of colors for each channel.
    num_colors = 256

    def __init__(self, eps: float = 1e-3, **kwargs):
        super().__init__(**kwargs)
        self.eps = eps

        self.reduction = 256 // self.num_colors

    def map(self, img: np.ndarray) -> Tuple[np.ndarray, ...]:
        shifted = img + self.eps
        normalized = 255 * shifted / np.max(shifted, axis=-1, keepdims=True) + 0.5
        normalized = ((normalized.astype(int) + self.reduction // 2) //
                      self.reduction * self.reduction).clip(max=255)
        color_index = normalized[..., 0] * 256 ** 2 + \
                      normalized[..., 1] * 256 + \
                      normalized[..., 2]

        grayscale = img.mean(axis=-1) + 0.5

        return color_index, grayscale.astype(np.uint8)


class fast(common):
    num_colors = 16
