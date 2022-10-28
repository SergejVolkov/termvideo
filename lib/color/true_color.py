from ..utils import ColorString


class ColorPalette:
    def __init__(self, code):
        self.code = code

    def __getitem__(self, i):
        r = i // 256 ** 2
        g = i // 256 % 256
        b = i % 256
        return ColorString(f"\033[{self.code};2;{r};{g};{b}m")


#: True color background palette.
back_palette = ColorPalette(48)

#: True color foreground palette.
fore_palette = ColorPalette(38)
