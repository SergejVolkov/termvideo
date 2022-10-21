import os
import ffmpeg
import numpy as np
import multiprocessing

from time import sleep
from playsound import playsound
from typing import Tuple, Dict
from collections import defaultdict

from .pool import pool2d
from .cursor import move_cursor
from .utils import perf_counter_ms
from .colors import color_palette
from .colors.cmap import common as cmap_common


class TerminalVideoCapture:
    """
    Terminal video decoder.

    The input video is converted into pseudographics using
    ASCII escape codes.

    Notice that the actual values of terminal colors depend
    on your color scheme. An imprecise guess is made based
    on standard schemes, so the colors may not be accurate!

    After initialization this class can be used as iterator
    to get a sequence of video frames converted to ASCII format.

    Args:
        path (str): Path to video.
        out_w (int): Width of the output device (number of columns).
        pix_aspect (Tuple[int, int]): Size of the output terminal
            character in (width, height). Defaults to (1, 2).
        cmap ((img: np.ndarray) -> np.ndarray): Color mapping function.
            Defaults to `colors.cmap.common`.
            Converts image of size (H, W, 3) into indexed color (H, W).
            See `colors` module for color indices.
        sleep_overhead (int): Approximate sleep function overhead in ms.
            Defaults to 10 ms.
        debug_stats (bool): Enable debug profiling. Defaults to False.

    """

    def __init__(self, path, out_w, pix_aspect = (1, 2),
                 cmap = cmap_common, sleep_overhead = 10,
                 debug_stats = False):
        self.path = path
        self.out_w = out_w
        self.pix_aspect = pix_aspect
        self.cmap = cmap
        self.sleep_overhead = sleep_overhead
        self.gather_debug_stats = debug_stats

        self.kernel = tuple(reversed(self.pix_aspect))
        self.reset_seq = move_cursor(0, 0)

        self.streaming = False

        meta = ffmpeg.probe(
            self.path,
            loglevel="error",
            select_streams="v:0"
        )

        self.src_w = meta["streams"][0]["width"]
        self.src_h = meta["streams"][0]["height"]
        self.out_h = (self.out_w * self.src_h * self.pix_aspect[0] //
                      self.src_w // self.pix_aspect[1])
        self.stream_w = self.out_w * self.pix_aspect[0]
        self.stream_h = self.out_h * self.pix_aspect[1]

        self.fps = eval(meta["streams"][0]["avg_frame_rate"])
        self.step = 1000 / self.fps

        self.cap = ffmpeg.input(self.path)

        self.video = self.cap.output(
            "pipe:",
            loglevel="error",
            format="rawvideo",
            pix_fmt="rgb24",
            vf=f"scale={self.stream_w}:{self.stream_h}:"
               f"flags={'area' if self.stream_w < self.src_w else 'bicubic'}"
        ).run_async(pipe_stdout=True)

        self.audio_path = os.environ.get("TEMP") + "/" + \
            os.path.splitext(os.path.basename(path[:-3]))[0] + ".wav"
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
        self.cap.output(
            self.audio_path,
            loglevel="error",
            vn=None,
        ).run()

    def __iter__(self):
        """
        Start video & audio stream.

        """
        self.streaming = True
        self.frames_read = 0

        self.audio = multiprocessing.Process(target=playsound,
                                             args=(self.audio_path, ))
        self.audio.start()
        self.start_time = perf_counter_ms()

        if self.gather_debug_stats:
            self._debug_info = defaultdict(int)
        return self

    def __next__(self) -> str:
        """
        Read next frame in sync with source timestamps.

        Timestamps are estimated using ffprobe's average
        frame rate. Videos with variable frame rate may
        get out of sync with audio!

        Returns:
            str: Next synced frame encoded into ASCII.

        """
        if self.gather_debug_stats:
            start = perf_counter_ms()
            wait_time = self.wait_time

        # Synchronize video by waiting or dropping frames
        if self.wait_time < -self.step:
            while self.wait_time <= 0:
                self.drop_frame()
        else:
            if self.wait_time > self.sleep_overhead:
                sleep((self.wait_time - self.sleep_overhead) / 1000)
            while self.wait_time > 0:
                pass

        if self.gather_debug_stats:
            self._debug_info["required sleep"] += wait_time
            self._debug_info["actual sleep"] += perf_counter_ms() - start
            start = perf_counter_ms()

        # Read next frame from stream
        frame = np.frombuffer(self.read_frame(), dtype=np.uint8)
        frame = frame.reshape(self.stream_h, self.stream_w, 3)

        if self.gather_debug_stats:
            self._debug_info["ffmpeg"] += perf_counter_ms() - start
            start = perf_counter_ms()

        # Convert to output terminal character aspect ratio
        scaled = pool2d(frame.astype(np.float32), self.kernel, method="mean")

        if self.gather_debug_stats:
            self._debug_info["pool"] += perf_counter_ms() - start
            start = perf_counter_ms()

        # Convert to indexed color
        scaled = self.cmap(scaled).flatten()

        # Lower the number of escape codes by squashing
        # constant color sequences into one value
        mask = np.ones(scaled.shape[0] + 1, dtype=bool)
        mask[1:-1] = (scaled[1:] != scaled[:-1])
        compressed = scaled[mask[:-1]]
        counts = np.flatnonzero(mask)
        counts = counts[1:] - counts[:-1]

        if self.gather_debug_stats:
            self._debug_info["np convert"] += perf_counter_ms() - start
            start = perf_counter_ms()

        # Form the output string
        converted = "".join([self.reset_seq] +
                            [color_palette[c] + " " * count
                             for c, count in zip(compressed, counts)])

        if self.gather_debug_stats:
            self._debug_info["py convert"] += perf_counter_ms() - start
        return converted

    def read_frame(self) -> bytes:
        """
        Read next frame from stream.

        Returns:
            bytes: Raw frame data.

        """
        self.frames_read += 1

        frame = self.video.stdout.read(self.stream_w * self.stream_h * 3)
        if not frame:
            self.release()
            raise StopIteration
        return frame

    def drop_frame(self):
        """
        Drop video frame.

        """
        if self.gather_debug_stats:
            self._debug_info["frame drop ratio"] += 1

        self.read_frame()

    def release(self):
        """
        Stop the playback by terminating open streams.

        """
        if self.streaming:
            self.video.terminate()
            self.audio.terminate()
            sleep(0.1)
            os.remove(self.audio_path)

            self.streaming = False

    @property
    def timestamp(self) -> int:
        """
        Current frame timestamp.

        Returns:
            int: Current timestamp in ms.

        """
        return int(self.frames_read * self.step)

    @property
    def wait_time(self) -> int:
        """
        Time till the next frame.

        Returns:
            int: Wait time in ms.

        """
        return self.timestamp - (perf_counter_ms() - self.start_time)

    @property
    def debug_stats(self):
        """
        Debug statistics.

        Returns:
            Dict: Dictionary of debug stats.

        Raises:
            ValueError: If debug mode is not activated.

        """
        if not self.gather_debug_stats:
            raise ValueError("debug mode not active")
        return {key: val / self.frames_read for key, val in self._debug_info.items()}
