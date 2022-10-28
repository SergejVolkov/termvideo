import numpy as np
from typing import Sequence, Tuple

from ..utils import move_cursor, interlace_index
from .base import abstractmethod, base_cmap


class base_multi_cmap(base_cmap):
    def __init__(self, interlaced: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.interlaced = interlaced

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

    def compress(self, index: Tuple[np.ndarray, ...]) \
            -> Tuple[Sequence[Sequence], Sequence[Sequence], int, int]:
        values = []
        counts = []
        h, w = index[0].shape
        running_mask = np.zeros(h * w + 1, dtype=bool)
        if self.interlaced:
            running_mask[np.arange(0, running_mask.shape[0], w)] = True
        for i, idx in enumerate(index):
            if self.interlaced:
                idx = np.concatenate((idx[::2], idx[1::2]), axis=0)
            idx = idx.flatten()
            mask = np.ones(idx.shape[0] + 1, dtype=bool)
            mask[1:-1] = (idx[1:] != idx[:-1])
            running_mask |= mask
            if i == len(index) - 1:
                mask = running_mask
            values.append(idx[mask[:-1]])
            counts_ = np.flatnonzero(mask)
            counts.append(counts_)
        counts[-1] = counts_[1:] - counts_[:-1]
        return values, counts, w, h

    def to_string(self, compressed: Tuple[Sequence[Sequence],
                                          Sequence[Sequence],
                                          int, int]) -> str:
        values, counts, w, h = compressed
        cvalues, tvalues = values[:-1], values[-1]
        ccounts, tcounts = counts[:-1], counts[-1]

        if self.interlaced:
            row_idx = interlace_index(w, h)

        chunks = [] if self.interlaced else [self.reset_seq]
        vidx = [0] * len(cvalues)
        i = 0
        for value, count in zip(tvalues, tcounts):
            if self.interlaced and i % w == 0:
                chunks.append(move_cursor(0, row_idx(i) + 1))
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
