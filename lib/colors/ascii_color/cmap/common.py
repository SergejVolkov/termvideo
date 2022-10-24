import numpy as np

from ..palette import acolor_rgb_norm, ascii_grayscale


def common(img: np.ndarray) -> np.ndarray:
    """
    Convert RGB image of size (H, W, 3) to indexed color (H, W).

    See `colors.ascii_color.palette` for details on color palette.

    Args:
        img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
            `dtype=np.uint8`.

    Returns:
        np.ndarray: Image in indexed color format.

    """
    normalized = img / np.expand_dims(img.max(axis=-1), -1)
    normalized = np.expand_dims(normalized, -2)
    acolor_index = np.argmin(
        np.abs(normalized - np.expand_dims(acolor_rgb_norm, (0, 1))).mean(axis=-1),
        axis=-1
    )
    agrayscale_raw = img.mean(axis=-1)
    agrayscale_index = np.searchsorted(ascii_grayscale, agrayscale_raw).clip(max=len(ascii_grayscale) - 1)
    out = acolor_index * len(ascii_grayscale) + agrayscale_index
    return out
