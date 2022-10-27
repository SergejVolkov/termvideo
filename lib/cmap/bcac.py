import numpy as np
from typing import Tuple

from ..color.ascii import gradient, brightness_values
from ..color.terminal import rgb_values, back_palette, fore_palette
from .base_multi import base_multi_cmap


class common(base_multi_cmap):
    #: Combined palette.
    palette = [back_palette, fore_palette, gradient]

    def __init__(self, eps: float = 1e-3, **kwargs):
        super().__init__(**kwargs)
        self.eps = eps

    def map(self, img: np.ndarray) -> Tuple[np.ndarray, ...]:
        with self.profiler["map: bcolor index"]:
            bcolor_index = np.argmin(
                np.abs(np.expand_dims(img, -2) - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1),
                axis=-1
            )
            bcolor = rgb_values[bcolor_index]

        with self.profiler["map: brightness"]:
            diff = np.expand_dims(bcolor - img, -2)
            num = (255 * diff).mean(axis=-1)
            denom = (np.expand_dims(bcolor, -2) -
                     np.expand_dims(rgb_values, (0, 1))).mean(axis=-1) + self.eps
            brightness = (num / denom).clip(min=0, max=brightness_values[-1])

        with self.profiler["map: fcolor index"]:
            fcolor_index = np.argmin(
                np.abs(diff + np.expand_dims(rgb_values, (0, 1)) *
                       np.expand_dims(brightness, -1) / 255).mean(axis=-1),
                axis=-1
            )

        with self.profiler["map: brightness index"]:
            brightness = np.take_along_axis(
                brightness,
                np.expand_dims(fcolor_index, -1),
                axis=-1
            )
            brightness_index = np.searchsorted(brightness_values, brightness)

        return (bcolor_index.astype(np.uint8),
                fcolor_index.astype(np.uint8),
                brightness_index.astype(np.uint8))
