import math
import numpy as np


def pool2d(x, kernel, method= "max", pad=False):
    """
    Non-overlapping pooling on 2D or 3D data.

    By Jason https://stackoverflow.com/a/49317610

    x (np.ndarray): input array to pool.
    kernel (tuple): kernel size in (ky, kx).
    method (str): "max" for max-pooling,
        "mean" for mean-pooling.
    pad (bool): pad `x` or not. If no pad, output has size
        n // f, n being `x` size, f being kernel size.
        if pad, output has size ceil(n / f).

    Returns:
        result: pooled matrix.

    """
    m, n = x.shape[:2]
    ky, kx = kernel

    def ceil(x, y):
        return int(math.ceil(x / y))

    if pad:
        ny = ceil(m, ky)
        nx = ceil(n, kx)
        size = (ny * ky, nx * kx) + x.shape[2:]
        x_pad = np.full(size, np.nan)
        x_pad[:m, :n, ...] = x
    else:
        ny = m // ky
        nx = n // kx
        x_pad = x[:ny * ky, :nx * kx, ...]

    new_shape = (ny, ky, nx, kx) + x.shape[2:]

    if method == "max":
        operation = np.nanmax if pad else np.max
    else:
        operation = np.nanmean if pad else np.mean
    result = operation(x_pad.reshape(new_shape), axis=(1, 3))

    return result
