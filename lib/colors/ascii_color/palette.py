from colorama import Fore

from ..back_color import Color, rgb_values
from ..ascii import palette as ascii_palette, grayscale_values as ascii_grayscale


class ColorString(str):
    def __new__(cls, value, *args, **kwargs):
        return super(ColorString, cls).__new__(cls, value)

    def __init__(self, values, fill: str = " "):
        self.fill = fill

    def __mul__(self, value):
        return self + self.fill * value


class ColorPalette:
    def __getitem__(self, i):
        acolor_index = i // len(ascii_grayscale)
        agrayscale_index = i % len(ascii_grayscale)
        return ColorString(acolor_palette[acolor_index],
                           fill=ascii_palette[agrayscale_index])


#: Foreground color + ASCII palette.
palette = ColorPalette()

#: Foreground color palette.
acolor_palette = [getattr(Fore, c.name) for c in Color
                  if c not in [Color.BLACK,
                               Color.WHITE,
                               Color.LIGHTBLACK_EX]]

#: Foreground color RGB values.
acolor_rgb = rgb_values[[i for i in range(len(Color))
                         if i not in [Color.BLACK.value,
                                      Color.WHITE.value,
                                      Color.LIGHTBLACK_EX.value]]]

#: Normalized RGB values.
acolor_rgb_norm = acolor_rgb / acolor_rgb.max(axis=-1).reshape(-1, 1)
