import ctypes
import os
import sys

import pyperclip
import pyscreenshot as ImageGrab
import pytesseract
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

try:
    from pynotifier import Notification
except ImportError:
    pass


class Snipper(QtWidgets.QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle("TextShot")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self.setStyleSheet("background-color: black")
        self.setWindowOpacity(0.5)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        if self.start == self.end:
            return super().paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(QtGui.QColor(255, 255, 255, 100))
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        x1, x2 = sorted((self.start.x(), self.end.x()))
        y1, y2 = sorted((self.start.y(), self.end.y()))

        self.hide()
        shot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        processImage(shot)
        QtWidgets.QApplication.quit()


def processImage(img):
    try:
        result = pytesseract.image_to_string(
            img, timeout=2, lang=(sys.argv[1] if len(sys.argv) > 1 else None)
        )
    except RuntimeError as error:
        print(f"ERROR: An error occurred when trying to process the image: {error}")
        notify(f"An error occurred when trying to process the image: {error}")
        return

    if result:
        pyperclip.copy(result)
        print(f'INFO: Copied "{result}" to the clipboard')
        notify(f'Copied "{result}" to the clipboard')
    else:
        print(f"INFO: Unable to read text from image, did not copy")
        notify(f"Unable to read text from image, did not copy")


def notify(msg):
    try:
        Notification(title="TextShot", description=msg).send()
    except (SystemError, NameError):
        pass


if __name__ == "__main__":
    try:
        pytesseract.get_tesseract_version()
    except EnvironmentError:
        notify(
            "Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        print(
            "ERROR: Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        sys.exit()

    if os.name == "nt":
        ctypes.windll.user32.SetProcessDPIAware()

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    snipper = Snipper(window)
    snipper.show()
    sys.exit(app.exec_())
