# TextShot

This tool gives users the ability to take a screenshot and copy to the clipboard the text content of the screenshot.

## Use

Running `textshot.py` will open an overlay over the screen, where a rectangle can be drawn over the portion of the screen containing the text the user wishes to copy.

It is recommended to attach a global hotkey to this tool. One can accomplish this by using an [AutoHotkey](https://www.autohotkey.com/) script on Windows; `textshot.ahk` contains a sample AHK script that can be used.

## Installation

- Install [Python 3](https://www.python.org/downloads/)
- Clone this repository, and `cd` into it
- (Optional) Create a virtual environment, for example with `python -m venv .venv`
- Install the required packages with `pip install -r requirements.txt`
- Install [Google's Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract), and ensure that `tesseract` can be reached from the command line by adding the directory to your system path.
