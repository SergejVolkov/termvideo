import numpy as np

from ..color_palette import Color


def lagtrain(img: np.ndarray, back: int = 178,
             eps: tuple = (6, 7)) -> np.ndarray:
    grayscale = img.mean(axis=-1)
    out = np.full_like(grayscale, Color.LIGHTBLACK_EX.value, dtype=np.uint8)
    out[back + eps[1] < grayscale] = Color.LIGHTWHITE_EX.value
    out[grayscale < back - eps[0]] = Color.BLACK.value
    return out
