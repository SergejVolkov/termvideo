from colorama import Fore

from ..back_color import Color, palette as bcolor_palette, rgb_values
from ..ascii import palette as ascii_palette, brightness_values as ascii_brightness
from ..ascii_color import ColorString


class ColorPalette:
    def __getitem__(self, i):
        bcolor_index = i // (len(ascii_brightness) * len(bcolor_palette))
        acolor_index = (i // len(ascii_brightness)) % len(bcolor_palette)
        abrightness_index = i % len(ascii_brightness)
        return ColorString(bcolor_palette[bcolor_index] + acolor_palette[acolor_index],
                           fill=ascii_palette[abrightness_index])


#: Combined background color + foreground color + ASCII palette.
palette = ColorPalette()

#: ASCII foreground color code strings.
acolor_palette = [getattr(Fore, c.name) for c in Color]