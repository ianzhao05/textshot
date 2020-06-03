<h1 align="center">TextShot</h2>

<div align="center">
<a href="https://github.com/ianzhao05/textshot/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ianzhao05/textshot"></a>
<a href="https://github.com/ianzhao05/textshot/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ianzhao05/textshot"></a>
<a href="https://github.com/ianzhao05/textshot/blob/master/LICENSE.txt"><img alt="GitHub license" src="https://img.shields.io/github/license/ianzhao05/textshot"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</div>

This tool gives users the ability to take a screenshot and copy to the clipboard the text content of the screenshot. Works on Windows, macOS, Ubuntu, Manjaro, and (should work on) most other Linux distros.

![TextShot Demo](https://i.imgur.com/Z0Ng13S.gif)

## Use

Running `textshot.py` will open an overlay over the screen, where a rectangle can be drawn over the portion of the screen containing the text the user wishes to copy.

An optional command line argument can specify the language. For example, `python textshot.py eng+fra` will use English as the primary language and French as the secondary language. The default is `eng` (English). Make sure that the appropriate data files for Tesseract are installed for other languages.

It is recommended to attach a global hotkey to this tool.

On **Windows**, one can accomplish this by using an [AutoHotkey](https://www.autohotkey.com/) script; `textshot.ahk` contains a sample AHK script that can be used.  
On **Ubuntu**, open the Keyboard Settings, which shows you all the Gnome shortcuts. At the bottom there is a `+` button to add your own shortcuts. Click it and set the command to `/usr/bin/python3 <path-to-textshot.py>`. In case you are using a venv, the python3 path above should point to the venv's python3 instead of the global python3.

## Installation

- Install [Python 3](https://www.python.org/downloads/)
- Clone this repository, and `cd` into it
- (Optional) Create a virtual environment, for example with `python -m venv .venv`
- Install the required packages with `pip install -r requirements.txt`
- Install [Google's Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract), and ensure that `tesseract` can be reached from the command line by adding the directory to your system path.

@rigred has added this to the AUR, so Arch Linux users can install the package `textshot-git` with their AUR helper. For example, `yay -S textshot-git`.
