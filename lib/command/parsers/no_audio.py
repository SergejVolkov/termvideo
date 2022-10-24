from .base import BaseParser


class NoAudioParser(BaseParser):
    def __init__(self):
        super().__init__(
            name=None,
            mapping={"no_audio": True,
                     "na": True},
            default=False,
            shortened=False
        )
