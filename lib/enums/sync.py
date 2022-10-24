from enum import Enum


class Sync(Enum):
    DROP_FRAMES = 0
    RESAMPLE_AUDIO = 1
    NONE = 2
