from enum import Enum


class Sync(Enum):
    DROP_FRAMES = 0
    RESAMPLE_AUDIO = 1
    NONE = 2

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def from_string(s):
        try:
            return Sync[s.upper()]
        except KeyError:
            raise ValueError(f"no such option {s}")
