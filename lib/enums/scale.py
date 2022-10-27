from enum import Enum


class Scale(Enum):
    RESIZE = 0
    STRETCH = 1
    CROP = 2
    FIT_WINDOW = 3

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def from_string(s):
        try:
            return Scale[s.upper()]
        except KeyError:
            raise ValueError(f"no such option {s}")
