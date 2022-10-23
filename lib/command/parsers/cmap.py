from .base import BaseParser
from ..option import Option
from lib.colors import cmap


class CmapParser(BaseParser):
    def __init__(self, shortened: bool = False):
        super().__init__(
            name="cmap",
            mapping=None,
            default=cmap.common,
            unwrapped=False,
            shortened=shortened
        )

    def __call__(self, option: Option) -> int:
        if (option.name == self._name or
                (self._shortened and option.name == self._name[0])):
            try:
                return getattr(cmap, option.value)
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
