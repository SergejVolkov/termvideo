import numpy as np

from ..color_palette import Color


def bad_apple(img: np.ndarray) -> np.ndarray:
    grayscale = img.mean(axis=-1)
    out = (grayscale > 255 / 2).astype(np.uint8) * Color.LIGHTWHITE_EX.value
    return out
