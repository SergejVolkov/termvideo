import os
import numpy as np


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
