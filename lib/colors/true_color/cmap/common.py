import numpy as np


def common(img: np.ndarray) -> np.ndarray:
    """
    Convert RGB image of size (H, W, 3) to indexed color (H, W).

    See `colors.true_color.palette` for details on color palette.

    Args:
        img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
            `dtype=np.uint8`.

    Returns:
        np.ndarray: Image in indexed color format.

    """
    img = img.astype(int)
    out = img[..., 0] * 256 ** 2 + img[..., 1] * 256 + img[..., 2]
    return out
