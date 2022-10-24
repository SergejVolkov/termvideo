import numpy as np

from ..palette import palette


BLACK = palette.index(" ")
WHITE = palette.index("@")


def bad_apple(img: np.ndarray) -> np.ndarray:
    grayscale = img.mean(axis=-1)
    out = (grayscale > 255 / 2).astype(np.uint8) * WHITE
    return out
