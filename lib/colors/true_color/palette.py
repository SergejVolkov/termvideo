from ..ascii_color import ColorString


class ColorPalette:
    def __getitem__(self, i):
        r = i // 256 ** 2
        g = i // 256 % 256
        b = i % 256
        return ColorString(f"\033[48;2;{r};{g};{b}m")


#: Foreground color + ASCII palette.
palette = ColorPalette()
