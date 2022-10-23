from .base import BaseParser


class StatsParser(BaseParser):
    def __init__(self):
        super().__init__(
            name=None,
            mapping={"stats": True},
            default=False,
            shortened=False
        )
