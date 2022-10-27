import numpy as np
from typing import Sequence, Tuple

from .base import abstractmethod, base_cmap


class base_single_cmap(base_cmap):
    @abstractmethod
    def map(self, img: np.ndarray) -> np.ndarray:
        """
        Convert RGB image of size (H, W, 3) to indexed color (H, W).

        Args:
            img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
                `dtype=np.uint8`.

        Returns:
            np.ndarray: Image in indexed color format.

        """
        pass

    @staticmethod
    def compress(index: np.ndarray) -> Tuple[Sequence, Sequence]:
        index = index.flatten()
        mask = np.ones(index.shape[0] + 1, dtype=bool)
        mask[1:-1] = (index[1:] != index[:-1])
        values = index[mask[:-1]]
        counts = np.flatnonzero(mask)
        counts = counts[1:] - counts[:-1]
        return values, counts

    def to_string(self, compressed: Tuple[Sequence, Sequence]) -> str:
        values, counts = compressed
        return "".join([self.reset_seq] +
                       [self.palette[c] * count
                        for c, count in zip(values, counts)])

    @property
    @abstractmethod
    def palette(self) -> Sequence:
        pass
