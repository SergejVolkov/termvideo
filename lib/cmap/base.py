import numpy as np

from typing import Any
from abc import ABC, abstractmethod

from ..utils import move_cursor
from ..profile import Profile


class base_cmap(ABC):
    reset_seq = move_cursor(0, 0)

    def __init__(self, profiler = None):
        self.profiler = Profile(enabled=False) if profiler is None else profiler

    def __call__(self, img: np.ndarray):
        with self.profiler["map"]:
            index = self.map(img)
        with self.profiler["compress"]:
            compressed = self.compress(index)
        with self.profiler["to string"]:
            converted = self.to_string(compressed)
        return converted

    def __str__(self):
        return f"{__name__}.{self.__name__}"

    @abstractmethod
    def map(self, img: np.ndarray):
        """
        Convert RGB image of size (H, W, 3) to indexed color (H, W).

        Args:
            img (np.ndarray): Input RGB image in (H, W, 3), [0, 255],
                `dtype=np.uint8`.

        Returns:
            Any: Image in indexed color format.

        """
        pass

    @staticmethod
    @abstractmethod
    def compress(index):
        """
        Compress image.

        Lower the number of escape codes by squashing
        constant color sequences into one value.

        Args:
            index (Any): Indexed color image.

        Returns:
            Any: Compressed representation.

        """
        pass

    @abstractmethod
    def to_string(self, compressed) -> str:
        pass

    @property
    @abstractmethod
    def palette(self):
        pass
