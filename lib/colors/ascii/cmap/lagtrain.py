import numpy as np

from ..palette import palette


BLACK = palette.index(" ")
GRAY  = palette.index("I")
WHITE = palette.index("@")


def lagtrain(img: np.ndarray, back: int = 178,
             eps: tuple = (11, 7)) -> np.ndarray:
    grayscale = img.mean(axis=-1)
    out = np.full_like(grayscale, GRAY, dtype=np.uint8)
    out[back + eps[1] < grayscale] = WHITE
    out[grayscale < back - eps[0]] = BLACK
    return out
