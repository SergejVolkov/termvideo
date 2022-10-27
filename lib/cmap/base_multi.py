import numpy as np
from typing import Sequence, Tuple

from .base import abstractmethod, base_cmap


class base_multi_cmap(base_cmap):
    @abstractmethod
    def map(self, img: np.ndarray) -> Tuple[np.ndarray, ...]:
        """
        Convert RGB image of size (H, W, 3) to indexed color (H, W).

        Args:
            img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
                `dtype=np.uint8`.

        Returns:
            Tuple[np.ndarray, ...]: Image in indexed color format.

        """
        pass

    @staticmethod
    def compress(index: Tuple[np.ndarray, ...]) \
            -> Tuple[Sequence[Sequence], Sequence[Sequence]]:
        values = []
        counts = []
        running_mask = None
        for i, idx in enumerate(index):
            idx = idx.flatten()
            mask = np.ones(idx.shape[0] + 1, dtype=bool)
            mask[1:-1] = (idx[1:] != idx[:-1])
            if running_mask is None:
                running_mask = mask
            else:
                running_mask |= mask
            if i == len(index) - 1:
                mask = running_mask
            values.append(idx[mask[:-1]])
            counts_ = np.flatnonzero(mask)
            counts.append(counts_)
        counts[-1] = counts_[1:] - counts_[:-1]
        return values, counts

    def to_string(self, compressed: Tuple[Sequence[Sequence],
                                          Sequence[Sequence]]) -> str:
        values, counts = compressed
        cvalues, tvalues = values[:-1], values[-1]
        ccounts, tcounts = counts[:-1], counts[-1]

        chunks = [self.reset_seq]
        vidx = [0] * len(cvalues)
        i = 0
        for value, count in zip(tvalues, tcounts):
            for vi in range(len(cvalues)):
                if i >= ccounts[vi][vidx[vi]]:
                    chunks.append(self.palette[vi][cvalues[vi][vidx[vi]]])
                    vidx[vi] += 1
            chunks.append(self.palette[-1][value] * count)
            i += count
        return "".join(chunks)

    @property
    @abstractmethod
    def palette(self) -> Sequence:
        pass
