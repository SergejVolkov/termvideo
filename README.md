# termvideo
Video player for command terminal built on ASCII color codes, FFmpeg & PyAudio.

[![alt text](https://raw.githubusercontent.com/SergejVolkov/termvideo/main/pic/lagtrain.jpg)](https://www.youtube.com/watch?v=4NcLxLAtIA0)

**Key features**

+ *Realtime playback with audio*
+ *Customizable color mappings for render*
+ *Cross-platform (tested in Windows 10 cmd.exe and Ubuntu 20.04 bash)*
+ *Correct aspect ratio processing*
+ *Playback speed control*
+ *Comprehensible usage manual*

## Installation

**Important!**

**This program requires FFmpeg installed & accessible via the `$PATH` environment variable! FFmpeg can be downloaded from [the official site](https://ffmpeg.org/download.html). On Windows FFmpeg folder should be [added to PATH](https://www.google.com/search?q=add+ffmpeg+to+path).**

To install Python head over to [www.python.org](https://www.python.org/downloads/release/python-3810/) to download Python 3.8.10 installer.

*Notice. The app is tested for Python 3.8, but will probably work with later Python versions.*

Then run the command:

`pip install -r requirements.txt`

If you use Anaconda, run the following commands:

`conda env create -f environment.yaml`\
`conda activate termvideo`

Run the program by:

`python termvideo.py FILENAME`

Stop the playback with `Ctrl+C`.

## Usage

Various color mappings (ways to convert video to terminal colors) can be applied via `--cmap` option (`-c` for short). For example, if you wish to display a video as ASCII art, use

`python termvideo.py FILENAME -c ascii`

`-c bca` for a hybrid ascii and background color cmap, `-c true_color` for the full RGB color (if your terminal supports it).

Several scaling options are available through command options, e.g. `-s crop`, `-s stretch`. See the full usage manual by running:

`python termvideo.py -h`

## TODO
+ Docstrings
