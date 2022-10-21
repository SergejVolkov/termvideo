import numpy as np

from ..color_palette import rgb_values


def common(img: np.ndarray) -> np.ndarray:
    img = np.expand_dims(img, -2)
    out = np.argmin(np.abs(img - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1), axis=-1)
    return out
