# termvideo
Video player for command terminal built on ASCII color codes, FFmpeg & PyAudio.

[alt text](https://raw.githubusercontent.com/SergejVolkov/termvideo/main/pic/bad_apple.png)

This is a short decription

**Key features**

+ *Some feature*

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

If you wish to convert a video to terminal colors in your own way, you can create a custom color mapping function using numpy. The function receives an RGB image in numpy format (channels last) and outputs the converted image. Head over to `colors.cmap` module to see the examples.

Several scaling options are available through command options. See full usage manual by running:

`python termvideo.py -h`

## TODO
+ Complete README
+ Docstrings
+ 'Crop' scaling mode
