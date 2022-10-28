import numpy as np

from .. import color
from .base_single import base_single_cmap


class common(base_single_cmap):
    #: True color palette.
    palette = color.true_color.back_palette

    #: Number of colors for each channel.
    num_colors = 256

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.reduction = 256 // self.num_colors

    def map(self, img: np.ndarray) -> np.ndarray:
        img = ((img.astype(int) + self.reduction // 2) //
               self.reduction * self.reduction).clip(max=255)
        out = img[..., 0] * 256 ** 2 + img[..., 1] * 256 + img[..., 2]
        return out


class fast(common):
    num_colors = 16
