from .base import BaseParser
from ..option import Option
from lib import colors


class CmapParser(BaseParser):
    def __init__(self):
        super().__init__(
            name="cmap",
            mapping=None,
            default=(colors.back_color.cmap.common,
                     colors.back_color.palette),
            unwrapped=False,
            shortened=False
        )

    def __call__(self, option: Option) -> tuple:
        if (option.name == self._name or
                (self._shortened and option.name == self._name[0])):
            try:
                path = option.value.split(".")
                module = getattr(colors, path[0])
                if len(path) > 1:
                    return getattr(module.cmap, path[1]), module.palette
                return getattr(module.cmap, "common"), module.palette
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
