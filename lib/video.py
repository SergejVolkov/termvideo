# import cv2
import ffmpeg
import pyaudio
import numpy as np

from time import sleep
from typing import Tuple, List

from .utils import move_cursor, get_optimal_size, \
    perf_counter_ms, GracefulKiller
from .colors import back_color
from .enums import Scale, Sync
from .profile import Profile, Format


class ASCIIVideoCapture:
    """
    Class for video capturing and converting it into text.

    The input video is converted into text-based semigraphics
    using ASCII escape codes.

    Notice that the actual values of terminal colors depend
    on your color scheme. An imprecise guess is made based
    on standard schemes, so the colors may not be accurate!

    After initialization this class can be used as iterator
    to get a sequence of video frames converted to ASCII format.

    Args:
        path (str): Path to video.
        out_size (Tuple[int, int]): Size of the output device in
            (columns, lines). Defaults to None (auto). Either columns
            or lines can be set to None to be deduced from the video size.
        chr_aspect (Tuple[int, int]): Size of the output terminal
            character in (width, height). Defaults to (1, 2).
        cmap ((img: np.ndarray) -> np.ndarray): Color mapping function.
            Defaults to `colors.back_color.cmap.common`.
            Converts RGB image of size (H, W, 3) to indexed color (H, W).
            See `colors` module for details.
        palette (List[str]): String color values. Defaults to
            `colors.back_color.palette`. See `colors` module for details.
        speed (float): Playback speed. Defaults to 1.
        no_audio (bool): Do not play audio track. Defaults to False.
        sync (Sync): Video sync method. Defaults to `Sync.DROP_FRAMES`.
        sleep_overhead (int): Approximate `time.sleep` overhead in ms.
            Defaults to 10 ms.
        audio_bit_depth (int): Output audio sample size in bits.
            Defaults to 16-bit audio.
        profiler (Profile): Debug profiler.
            Defaults to None (profiling disabled).

    """

    def __init__(self, path, out_size = None, chr_aspect = (1, 2),
                 cmap = back_color.cmap.common, palette = back_color.palette,
                 speed = 1, no_audio = False, sync = Sync.DROP_FRAMES,
                 sleep_overhead = 10, audio_bit_depth = 16, profiler = None):
        self.path = path
        self.out_size = out_size
        self.chr_aspect = chr_aspect
        self.cmap = cmap
        self.palette = palette
        self.speed = speed
        self.no_audio = True if self.speed != 1 else no_audio
        self.sync = sync
        self.sleep_overhead = sleep_overhead
        self.audio_bit_depth = audio_bit_depth
        self.profiler = Profile(enabled=False) if profiler is None else profiler

        self.profiler["frames dropped"].formatting = Format.PERCENT, "%.1f"

        self.kernel = tuple(reversed(self.chr_aspect))
        self.audio_byte_depth = self.audio_bit_depth // 8

        self.reset_seq = move_cursor(0, 0)

        self.killer = GracefulKiller()
        self.streaming = False

        meta = ffmpeg.probe(
            self.path,
            loglevel="error"
        )
        self.cap = ffmpeg.input(self.path)

        # v:0
        self.video_meta = [stream for stream in meta["streams"]
                           if stream["codec_type"] == "video"][0]
        self.src_w = self.video_meta["width"]
        self.src_h = self.video_meta["height"]
        if self.out_size is None:
            self.out_w, self.out_h = get_optimal_size(self.src_w,
                                                      self.src_h,
                                                      self.chr_aspect)
        elif self.out_size[1] is None:
            self.out_w = self.out_size[0]
            self.out_h = (self.out_w * self.src_h * self.chr_aspect[0] //
                          (self.src_w * self.chr_aspect[1]))
        elif self.out_size[0] is None:
            self.out_h = self.out_size[1]
            self.out_w = (self.out_h * self.src_w * self.chr_aspect[1] //
                          (self.src_h * self.chr_aspect[0]))
        else:
            self.out_w, self.out_h = self.out_size

        self.fps = eval(meta["streams"][0]["avg_frame_rate"])
        self.step = 1000 / self.fps / self.speed

        self.video = self.cap.output(
            "pipe:",
            loglevel="error",
            format="rawvideo",
            pix_fmt="rgb24",
            vf=f"scale={self.out_w}:{self.out_h}:"
               f"flags={'area' if self.out_w < self.src_w else 'bicubic'}"
        ).run_async(pipe_stdout=True)

        # a:0
        if self.no_audio:
            self.audio = None
            return

        try:
            self.audio_meta = [stream for stream in meta["streams"]
                               if stream["codec_type"] == "audio"][0]
            self.sample_rate = int(self.audio_meta["sample_rate"])
            self.audio_channels = self.audio_meta["channels"]
            self.audio_frame_size = self.audio_byte_depth * self.audio_channels
        except IndexError:
            # No audio track
            self.audio = None
            return

        self.audio = self.cap.output(
            "pipe:",
            loglevel="error",
            format=f"s{self.audio_bit_depth}le",
            sample_rate=f"{self.sample_rate}"
        ).run_async(pipe_stdout=True)

        try:
            def callback(in_data, frame_count, time_info, status):
                data = self.audio.stdout.read(frame_count * self.audio_frame_size)
                if not data:
                    return data, pyaudio.paComplete
                return data, pyaudio.paContinue

            self.pyaudio = pyaudio.PyAudio()
            self.pyaudio_stream = self.pyaudio.open(
                format=self.pyaudio.get_format_from_width(self.audio_byte_depth,
                                                          unsigned=False),
                channels=self.audio_channels,
                rate=self.sample_rate,
                output=True,
                stream_callback=callback
            )
        except (ffmpeg.Error, OSError):
            # Output device missing, etc
            self.audio.terminate()
            self.audio = None

    def __iter__(self):
        """
        Start video & audio stream.

        """
        self.streaming = True
        self.frames_read = 0

        if self.audio is not None:
            self.pyaudio_stream.start_stream()
        self.start_time = perf_counter_ms()

        return self

    def __next__(self) -> str:
        """
        Read next frame in sync with source timestamps.

        Timestamps are estimated using ffprobe average
        frame rate. Videos with variable frame rate may
        get out of sync with audio!

        Returns:
            str: Next synced frame encoded to ASCII.

        """
        # Stop playback upon receiving termination signal
        if self.killer.kill_now:
            raise StopIteration

        # Synchronize video by waiting or dropping frames
        self.profiler["required sleep"] += self.wait_time * 1e6
        self.profiler["frames dropped"].n_runs = self.frames_read

        with self.profiler["actual sleep"]:
            if self.wait_time < -self.step:
                if self.sync == Sync.DROP_FRAMES:
                    while self.wait_time <= 0:
                        self.drop_frame()
                elif self.sync != Sync.NONE:
                    raise NotImplementedError(f"sync method {self.sync} not implemented")
            else:
                if self.wait_time > self.sleep_overhead:
                    sleep((self.wait_time - self.sleep_overhead) / 1000)
                while self.wait_time > 0:
                    pass

        # Read next frame from stream
        with self.profiler["ffmpeg"]:
            frame = np.frombuffer(self.read_frame(), dtype=np.uint8)
            frame = frame.reshape(self.out_h, self.out_w, 3)
            # if self.frames_read % 40 == 0:
            #     cv2.imwrite(f"output/frame_{self.frames_read}.png", frame)

        with self.profiler["np convert"]:
            # Convert to indexed color
            index = self.cmap(frame).flatten()

            # Lower the number of escape codes by squashing
            # constant color sequences into one value
            mask = np.ones(index.shape[0] + 1, dtype=bool)
            mask[1:-1] = (index[1:] != index[:-1])
            compressed = index[mask[:-1]]
            counts = np.flatnonzero(mask)
            counts = counts[1:] - counts[:-1]

        # Form the output string
        with self.profiler["py convert"]:
            converted = "".join([self.reset_seq] +
                                [self.palette[c] * count
                                 for c, count in zip(compressed, counts)])
        return converted

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False

    def read_frame(self) -> bytes:
        """
        Read next frame from stream.

        Returns:
            bytes: Raw frame data.

        """
        self.frames_read += 1

        frame = self.video.stdout.read(self.out_w * self.out_h * 3)
        if not frame:
            raise StopIteration
        return frame

    def drop_frame(self):
        """
        Drop video frame.

        """
        self.profiler["frames dropped"].total_value += 1

        self.read_frame()

    def release(self):
        """
        Stop the playback by terminating open streams.

        """
        if self.streaming:
            self.video.terminate()
            if self.audio is not None:
                self.pyaudio_stream.stop_stream()
                self.pyaudio_stream.close()
                self.pyaudio.terminate()
                self.audio.terminate()
            sleep(0.1)

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
