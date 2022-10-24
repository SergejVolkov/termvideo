from .base import BaseParser
from ..option import Option


class AspectParser(BaseParser):
    def __init__(self):
        super().__init__(
            name="aspect",
            mapping=None,
            default=(1, 2),
            unwrapped=False,
            shortened=False
        )

    def __call__(self, option: Option) -> tuple:
        if option.name == self._name:
            try:
                pair = option.value.split(",")
                return int(pair[0]), int(pair[1])
            except BaseException:
                pass
        raise IndexError("no suitable conversion")
