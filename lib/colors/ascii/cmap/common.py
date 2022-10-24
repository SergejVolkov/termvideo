import numpy as np

from ..palette import grayscale_values


def common(img: np.ndarray, contrast: float = 0.) -> np.ndarray:
    """
    Convert RGB image of size (H, W, 3) to indexed color (H, W).

    See `colors.symbol.palette` for details on color palette.

    Args:
        img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
            `dtype=np.uint8`.
        contrast (float): Contrast setting in [0, 1].
            Defaults to 0 (no constrast manipulation).

    Returns:
        np.ndarray: Image in indexed color format.

    """
    grayscale = img.mean(axis=-1)
    scaled_values = (grayscale_values + 255 * contrast) / (1 + contrast)
    out = np.searchsorted(scaled_values, grayscale).clip(max=len(scaled_values) - 1)
    return out.astype(np.uint8)
