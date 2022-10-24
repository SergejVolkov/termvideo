from ..back_color import palette as bcolor_palette, rgb_values
from ..ascii import palette as ascii_palette, brightness_values as ascii_brightness
from ..ascii_color import ColorString


class ColorPalette:
    def __getitem__(self, i):
        bcolor_index = i // len(ascii_brightness)
        abrightness_index = i % len(ascii_brightness)
        return ColorString(bcolor_palette[bcolor_index],
                           fill=ascii_palette[abrightness_index])


#: Background color + ASCII palette.
palette = ColorPalette()
