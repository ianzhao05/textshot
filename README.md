# TextShot

This tool gives users the ability to take a screenshot and copy to the clipboard the text content of the screenshot.

## Use

Running `textshot.py` will open an overlay over the screen, where a rectangle can be drawn over the portion of the screen containing the text the user wishes to copy.

It is recommended to attach a global hotkey to this tool.  

On **Windows**, one can accomplish this by using an [AutoHotkey](https://www.autohotkey.com/) script; `textshot.ahk` contains a sample AHK script that can be used.  
On **Ubuntu**, open the Keyboard Settings, which shows you all the Gnome shortcuts. At the bottom there is a `+` button to add your own shortcuts. Click it and set the command to `/usr/bin/python3 <path-to-textshot.py>`. In case you are using a venv, the python3 path above should point to the venv's python3 instead of the global python3.

## Installation

- Install [Python 3](https://www.python.org/downloads/)
- Clone this repository, and `cd` into it
- (Optional) Create a virtual environment, for example with `python -m venv .venv`
- Install the required packages with `pip install -r requirements.txt`
- Install [Google's Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract), and ensure that `tesseract` can be reached from the command line by adding the directory to your system path.
