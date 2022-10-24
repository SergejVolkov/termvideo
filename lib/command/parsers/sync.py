from .base import BaseParser
from lib.enums import Sync


class SyncParser(BaseParser):
    def __init__(self):
        super().__init__(
            name="sync",
            mapping={"drop_frames": Sync.DROP_FRAMES,
                     "resample_audio": Sync.RESAMPLE_AUDIO,
                     "none": Sync.NONE},
            default=Sync.DROP_FRAMES,
            unwrapped=False,
            shortened=False
        )
