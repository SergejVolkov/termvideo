import numpy as np

from ..palette import rgb_values


def common(img: np.ndarray) -> np.ndarray:
    """
    Convert RGB image of size (H, W, 3) to indexed color (H, W).

    See `colors.back_color.palette` for details on color palette.

    Args:
        img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
            `dtype=np.uint8`.

    Returns:
        np.ndarray: Image in indexed color format.

    """
    img = np.expand_dims(img, -2)
    out = np.argmin(np.abs(img - np.expand_dims(rgb_values, (0, 1))).mean(axis=-1), axis=-1)
    return out.astype(np.uint8)
