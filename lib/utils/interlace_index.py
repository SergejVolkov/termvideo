import numpy as np


def ceil(x, y):
    return int(np.ceil(x / y))


class interlace_index:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h

        self.denom = w * ceil(h, 2)
        self.num = h - (h + 1) % 2

    def __call__(self, i: int):
        return i // self.w * 2 - i // self.denom * self.num
