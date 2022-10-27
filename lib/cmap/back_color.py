import numpy as np

from ..color.terminal import Color, rgb_values, back_palette
from .base_single import base_single_cmap
from .base_bad_apple import base_bad_apple_cmap
from .base_lagtrain import base_lagtrain_cmap


class common(base_single_cmap):
    #: Background color code strings.
    palette = back_palette

    def map(self, img: np.ndarray) -> np.ndarray:
        img = np.expand_dims(img, -2)
        out = np.argmin(np.abs(img - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1), axis=-1)
        return out.astype(np.uint8)


class bad_apple(base_bad_apple_cmap, common):
    white = Color.LIGHTWHITE_EX.value


class lagtrain(base_lagtrain_cmap, common):
    black = Color.BLACK.value
    gray = Color.WHITE.value
    white = Color.LIGHTWHITE_EX.value
