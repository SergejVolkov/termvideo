from colorama import Back

from .color import Color


class ColorString(str):
    def __mul__(self, value):
        return self + " " * value


#: ASCII background color code strings.
palette = [ColorString(getattr(Back, c.name)) for c in Color]
