import os
import sys
import ffmpeg

from multiprocessing import freeze_support

from lib.utils import get_manual, term_capture
from lib.video import ASCIIVideoCapture
from lib.enums import Scale, Sync
from lib.profile import Profile
from lib.command import Command, CmapParser, ScaleParser, AspectParser, \
    SpeedParser, NoAudioParser, SyncParser, StatsParser, HelpParser


if __name__ == "__main__":
    freeze_support()

    # Parse command options
    cmd = Command(" ".join(sys.argv))
    ((cmap, palette), scale, chr_aspect, speed,
     no_audio, sync, stats, help), args = cmd.parse_options(
        parsers=[CmapParser(), ScaleParser(), AspectParser(), SpeedParser(),
                 NoAudioParser(), SyncParser(), StatsParser(), HelpParser()]
    )

    # Print help note
    if help or len(args) == 0:
        print(get_manual(), end="")
        exit()

    # Path to video file
    path = args[0]

    # Profiler
    profiler = Profile(enabled=stats)

    # Video scaling
    out_size = None
    if scale == Scale.STRETCH:
        term_size = os.get_terminal_size()
        out_size = term_size.columns, term_size.lines
    elif scale == Scale.CROP:
        raise NotImplementedError(f"scaling method {scale} not implemented")

    try:
        # Capture video and init terminal
        with ASCIIVideoCapture(
            path,
            out_size,
            chr_aspect,
            cmap,
            palette,
            speed,
            no_audio,
            sync,
            profiler=profiler
        ) as cap, term_capture(cap.out_w, cap.out_h), profiler["total"]:
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
