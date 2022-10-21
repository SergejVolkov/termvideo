from .base import BaseParser
from lib.colors import cmap


class CmapParser(BaseParser):
    def __init__(self):
        super(CmapParser, self).__init__(
            name="cmap",
            mapping={"common": cmap.common,
                     "bad_apple": cmap.bad_apple,
                     "lagtrain": cmap.lagtrain},
            default=cmap.common,
            unwrapped=False,
            shortened=False
        )
