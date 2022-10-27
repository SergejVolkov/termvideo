import os
import numpy as np

from colorama import Back, Fore
from enum import Enum

from ..utils import ColorString


class Color(Enum):
    """
    Terminal color name enum.

    """

    BLACK           = 0
    RED             = 1
    GREEN           = 2
    YELLOW          = 3
    BLUE            = 4
    MAGENTA         = 5
    CYAN            = 6
    WHITE           = 7
    LIGHTBLACK_EX   = 8
    LIGHTRED_EX     = 9
    LIGHTGREEN_EX   = 10
    LIGHTYELLOW_EX  = 11
    LIGHTBLUE_EX    = 12
    LIGHTMAGENTA_EX = 13
    LIGHTCYAN_EX    = 14
    LIGHTWHITE_EX   = 15


if os.name == "nt":
    #: ASCII color RGB values.
    rgb_values = np.array([
        [ 12,  12,  12],  # 0  black
        [197,  15,  31],  # 1  red
        [ 19, 161,  14],  # 2  green
        [193, 156,   0],  # 3  yellow
        [  0,  55, 218],  # 4  blue
        [136,  23, 152],  # 5  magenta
        [ 58, 150, 221],  # 6  cyan
        [204, 204, 204],  # 7  white
        [118, 118, 118],  # 8  light black
        [231,  72,  86],  # 9  light red
        [ 22, 198,  12],  # 10 light green
        [249, 241, 165],  # 11 light yellow
        [ 59, 120, 255],  # 12 light blue
        [180,   0, 158],  # 13 light magenta
        [ 97, 214, 214],  # 14 light cyan
        [242, 242, 242]   # 15 light white
    ])
else:
    #: ASCII color RGB values.
    rgb_values = np.array([
        [  0,   0,   0],  # 0  black
        [128,   0,   0],  # 1  red
        [  0, 128,   0],  # 2  green
        [128, 128,   0],  # 3  yellow
        [  0,   0, 128],  # 4  blue
        [128,   0, 128],  # 5  magenta
        [  0, 128, 128],  # 6  cyan
        [192, 192, 192],  # 7  white
        [128, 128, 128],  # 8  light black
        [255,   0,   0],  # 9  light red
        [255, 255,   0],  # 10 light green
        [  0, 255,   0],  # 11 light yellow
        [  0,   0, 255],  # 12 light blue
        [255,   0, 255],  # 13 light magenta
        [  0, 255, 255],  # 14 light cyan
        [255, 255, 255]   # 15 light white
    ])

#: Background color code strings.
back_palette = [ColorString(getattr(Back, c.name)) for c in Color]

#: Foreground color code strings.
fore_palette = [ColorString(getattr(Fore, c.name)) for c in Color]

#: Foreground colors with unique hues.
_hcolor = [c for c in Color
           if c not in [Color.BLACK,
                        Color.WHITE,
                        Color.LIGHTBLACK_EX]]

#: Their color code strings.
hpalette = [getattr(Fore, c.name) for c in _hcolor]

#: Their RGB values.
hrgb_values = rgb_values[[c.value for c in _hcolor]]

#: Normalized RGB values.
hrgb_norm = hrgb_values / np.max(hrgb_values, axis=-1, keepdims=True)
