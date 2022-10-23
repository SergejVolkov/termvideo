from .base import BaseParser
from lib.scale import Scale


class ScaleParser(BaseParser):
    def __init__(self):
        super().__init__(
            name="scale",
            mapping={"resize": Scale.RESIZE,
                     "stretch": Scale.STRETCH,
                     "crop": Scale.CROP},
            default=Scale.RESIZE,
            unwrapped=False
        )
