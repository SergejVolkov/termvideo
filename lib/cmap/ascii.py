import numpy as np

from .. import color
from .base_single import base_single_cmap
from .base_bad_apple import base_bad_apple_cmap
from .base_lagtrain import base_lagtrain_cmap


class common(base_single_cmap):
    #: ASCII 256 colors palette.
    palette = color.ascii.palette

    black = color.ascii.palette.index(" ")
    gray  = color.ascii.palette.index("Z")
    white = color.ascii.palette.index("@")

    def map(self, img: np.ndarray) -> np.ndarray:
        out = img.mean(axis=-1) + 0.5
        return out.astype(np.uint8)


class bad_apple(base_bad_apple_cmap, common):
    pass


class lagtrain(base_lagtrain_cmap, common):
    pass


# class unicode(ascii):
#     #: Unicode 256 colors palette.
#     palette = color.unicode.palette
#
#     black = color.unicode.palette.index(" ")
#     gray  = color.unicode.palette.index("▌")
#     white = color.unicode.palette.index("█")


# class bad_apple_unicode(base_bad_apple, unicode):
#     pass


# class lagtrain_unicode(base_lagtrain, unicode):
#     pass


# common = ascii
# bad_apple = bad_apple_ascii
# lagtrain = lagtrain_ascii
