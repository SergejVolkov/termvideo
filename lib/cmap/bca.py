import numpy as np
from typing import Tuple

from ..color.ascii import gradient, brightness_values
from ..color.terminal import rgb_values, back_palette
from .base_multi import base_multi_cmap


class common(base_multi_cmap):
    """

    Args:
        text_color (int): Text foreground color in [0, 255].
        eps (float): Lol.
        **kwargs: Keyword arguments.

    """

    #: Combined palette.
    palette = [back_palette, gradient]

    def __init__(self, text_color: int = 204,
                 eps: float = 1e-3, **kwargs):
        super().__init__(**kwargs)
        self.text_color = text_color
        self.eps = eps

    def map(self, img: np.ndarray) -> Tuple[np.ndarray, ...]:
        with self.profiler["map: color index"]:
            color_index = np.argmin(
                np.abs(np.expand_dims(img, -2) - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1),
                axis=-1
            )
            color = rgb_values[color_index]
            cgrayscale = color.mean(axis=-1)

        with self.profiler["map: brightness"]:
            grayscale = img.mean(axis=-1)
            brightness = 255 * (grayscale - cgrayscale) / (self.text_color - cgrayscale + self.eps)
            brightness_index = np.searchsorted(
                brightness_values,
                brightness
            ).clip(max=len(brightness_values) - 1)

        return color_index.astype(np.uint8), brightness_index.astype(np.uint8)
