from .base import BaseParser


class HelpParser(BaseParser):
    def __init__(self):
        super().__init__(
            name=None,
            mapping={"help": True},
            default=False
        )
