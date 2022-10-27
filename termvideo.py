import os
import sys
import ffmpeg
import argparse

from typing import Tuple
from multiprocessing import freeze_support

from lib.utils import term_capture
from lib.video import ASCIIVideoCapture
from lib.enums import Scale, Sync
from lib import cmap, color
from lib.profile import Profile


def main():
    # Parse command options
    args = get_args()
    scale = args.scale
    stats = args.stats

    # Profiler
    profiler = Profile(enabled=stats)

    # Color mapping
    cmap = get_cmap(args.cmap)(profiler=profiler)

    try:
        # Capture video and init terminal
        with ASCIIVideoCapture(
                args.filename,
                None,
                args.aspect,
                cmap,
                scale,
                args.speed,
                args.no_audio,
                args.sync,
                profiler=profiler
        ) as cap, term_capture(cap.term_w, cap.term_h), profiler["total"]:
            # Play video
            for frame in cap:
                with profiler["display"]:
                    print(frame, end="")
                    sys.stdout.flush()
    except ffmpeg.Error as e:
        # Handle ffmpeg exceptions
        reraise = True
        try:
            msg = e.stderr.decode("ascii")[:-1]
            if "No such file or directory" in msg:
                reraise = False
            print(msg)
        except AttributeError:
            pass
        if e.args[0].startswith("ffprobe"):
            stats = False
        if reraise:
            raise e
    finally:
        # Print stats
        if stats:
            profiler["total"].n_runs = profiler["display"].n_runs
            profiler.print_stats()
            print("fps: %d" % round(1e9 / profiler["total"].value))


def get_cmap(s: str):
    path = s.split(".")
    module = getattr(cmap, path[0])
    if len(path) > 1:
        return getattr(module, path[1])
    return module.common


def get_args():
    def int_pair(s: str) -> Tuple[int, int]:
        pair = s.split(",")
        return int(pair[0]), int(pair[1])

    def get_cmap_list() -> list:
        cmap_list = []
        for mname in dir(cmap):
            if mname.startswith("_") or mname.startswith("base"):
                continue
            cmap_list += [mname]
            module = getattr(cmap, mname)
            for name in dir(module):
                if (not name.startswith("_") and
                        name != "common" and not name.startswith("base") and
                        getattr(module, name).__class__.__name__ == "ABCMeta"):
                    cmap_list += [f"{mname}.{name}"]
        return cmap_list

    parser = argparse.ArgumentParser(description="Play video in terminal.")
    parser.add_argument("filename", metavar="FILENAME", type=str, help="Path to video.")
    parser.add_argument("-c", "--cmap", metavar="CMAP_NAME", type=str,
                        choices=get_cmap_list(), default="back_color",
                        help="Color mapping from RGB to terminal "
                             "(default: %(default)s). Available cmaps are " +
                             ", ".join(get_cmap_list()) + ".")
    parser.add_argument("-s", "--scale", type=Scale.from_string, choices=list(Scale),
                        default=Scale.RESIZE, help="Video scaling method "
                                                   "(default: %(default)s).")
    parser.add_argument("-a", "--aspect", metavar="W,H", type=int_pair,
                        default="15,32", help="Size of the terminal character "
                                              "(default: %(default)s).")
    parser.add_argument("--speed", metavar="SPEED", type=float,
                        default=1, help="Playback speed "
                                        "(default: %(default)s).")
    parser.add_argument("-na", "--no_audio", dest="no_audio", action="store_true",
                        help="Do not play audio track.")
    parser.add_argument("--sync", type=Sync.from_string, choices=list(Sync),
                        default=Sync.DROP_FRAMES, help="Video sync method "
                                                       "(default: %(default)s).")
    parser.add_argument("--stats", dest="stats", action="store_true",
                        help="Show debug statistics, useful for profiling.")
    return parser.parse_args()


if __name__ == "__main__":
    freeze_support()
    main()
