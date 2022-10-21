import os
import sys
import ffmpeg

from multiprocessing import freeze_support

from lib.utils import init_terminal, reset_terminal
from lib.video import TerminalVideoCapture, perf_counter_ms
from lib.command import Command, CmapParser


if __name__ == "__main__":
    freeze_support()

    # Parse command options
    cmd = Command(" ".join(sys.argv))
    options, args = cmd.parse_options(parsers=[CmapParser()])
    cmap = options[0]
    path = args[0]

    # Init terminal
    init_terminal()

    try:
        # Create video stream
        term_size = os.get_terminal_size()
        cap = TerminalVideoCapture(path,
                                   term_size.columns,
                                   cmap=cmap,
                                   debug_stats=True)
        # Resize terminal window
        os.system(f"mode {cap.out_w},{cap.out_h}")

        # Play video
        i = 0
        display = 0
        tstart = perf_counter_ms()
        for frame in cap:
            start = perf_counter_ms()
            print(frame, end="")
            sys.stdout.flush()
            display += perf_counter_ms() - start
            i += 1
            if i > 100:
                break

        # Close stream
        cap.release()
    except ffmpeg.Error as e:
        reset_terminal()
        try:
            print(e.stderr.decode("ascii"))
        except AttributeError:
            pass
        raise e
    except BaseException as e:
        reset_terminal()
        raise e

    # Print stats
    total = (perf_counter_ms() - tstart) / i
    display /= i
    print(*["%s: %.1f" % (key, val) for key, val in cap.debug_stats.items()],
          "display: %.1f" % display,
          "total: %.1f" % total,
          "fps: %d" % round(1000 / total),
          "frames dropped: %d" % cap.frames_dropped, sep="\n")
