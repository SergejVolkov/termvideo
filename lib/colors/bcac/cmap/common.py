import numpy as np

from ..palette import rgb_values, ascii_brightness


def common(img: np.ndarray, eps: float = 1e-3) -> np.ndarray:
    bcolor_index = np.argmin(
        np.abs(np.expand_dims(img, -2) - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1),
        axis=-1
    )
    bcolor = rgb_values[bcolor_index]
    abrightness_raw = (255 * np.expand_dims(bcolor - img, -2).mean(axis=-1) /
                       ((np.expand_dims(bcolor, -2) - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1) + eps))
    abrightness_index = np.searchsorted(ascii_brightness, abrightness_raw).clip(max=len(ascii_brightness) - 1)
    acolor_index = np.argmin(
        np.abs(ascii_brightness[abrightness_index] - abrightness_raw),
        axis=-1
    )
    abrightness_index = np.take_along_axis(
        abrightness_index,
        np.expand_dims(acolor_index, -1),
        axis=-1
    ).reshape(bcolor_index.shape)
    out = bcolor_index * len(ascii_brightness) * len(rgb_values) + \
          acolor_index * len(ascii_brightness) + abrightness_index
    return out
