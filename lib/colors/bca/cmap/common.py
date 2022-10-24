import numpy as np

from ..palette import rgb_values, ascii_brightness


def common(img: np.ndarray, text_grayscale: int = 204) -> np.ndarray:
    """
    Convert RGB image of size (H, W, 3) to indexed color (H, W).

    See `colors.combine.palette` for details on color palette.

    Args:
        img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
            `dtype=np.uint8`.
        text_grayscale (int): Text foreground color in [0, 255].

    Returns:
        np.ndarray: Image in indexed color format.

    """
    bcolor_index = np.argmin(
        np.abs(np.expand_dims(img, -2) - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1),
        axis=-1
    )
    bcolor = rgb_values[bcolor_index]
    bgrayscale = bcolor.mean(axis=-1)
    grayscale = img.mean(axis=-1)
    abrightness_raw = 255 * (grayscale - bgrayscale) / (text_grayscale - bgrayscale)
    abrightness_index = np.searchsorted(ascii_brightness, abrightness_raw).clip(max=len(ascii_brightness) - 1)
    out = bcolor_index * len(ascii_brightness) + abrightness_index
    return out
