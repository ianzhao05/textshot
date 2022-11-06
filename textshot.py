#!/usr/bin/env python3
""" Take a screenshot and copy its text content to the clipboard. """

import sys
import pytesseract
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from util import (get_ocr_result, notify, notify_copied, print_copied,
                  send_ocr_result_to_clipboard)
import argparse


class Snipper(QtWidgets.QWidget):
    def __init__(self, parent, langs=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle("TextShot")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self._screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())

        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(),
                         QtGui.QBrush(self.getWindow()))
        self.setPalette(palette)

        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()
        self.langs = langs

    def getWindow(self):
        return self._screen.grabWindow(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
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

    def snipOcr(self):
        self.hide()

        ocr_result = self.ocrOfDrawnRectangle()
        if ocr_result:
            return ocr_result
        else:
            print(f"INFO: Unable to read text from image, did not copy")
            notify(f"Unable to read text from image, did not copy")

    def hide(self):
        super().hide()
        QtWidgets.QApplication.processEvents()

    def ocrOfDrawnRectangle(self):
        return get_ocr_result(self.getWindow().copy(
            min(self.start.x(), self.end.x()),
            min(self.start.y(), self.end.y()),
            abs(self.start.x() - self.end.x()),
            abs(self.start.y() - self.end.y()),
        ), self.langs)


class OneTimeSnipper(Snipper):
    """ Take an OCR screenshot once then end execution. """

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        ocr_result = self.snipOcr()
        if ocr_result:
            send_ocr_result_to_clipboard(ocr_result)
            print_copied(ocr_result)
            notify_copied(ocr_result)
        QtWidgets.QApplication.quit()


class IntervalSnipper(Snipper):
    """ 
    Draw the screenshot rectangle once, then perform OCR there every `interval` 
    ms.
    """

    prevOcrResult = None

    def __init__(
            self,
            parent,
            interval,
            langs=None,
            flags=Qt.WindowFlags()):
        super().__init__(parent, langs, flags)
        self.interval = interval

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        # Take a shot as soon as the rectangle has been drawn
        self.onShotOcrInterval()
        # And then every `self.interval`ms
        self.startShotOcrInterval()

    def startShotOcrInterval(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.onShotOcrInterval)
        self.timer.start(self.interval)

    def onShotOcrInterval(self):
        prev_ocr_result = self.prevOcrResult
        ocr_result = self.snipOcr()

        self.prevOcrResult = ocr_result

        if not ocr_result or prev_ocr_result == ocr_result:
            return
        else:
            send_ocr_result_to_clipboard(ocr_result)
            print_copied(ocr_result)


arg_parser = argparse.ArgumentParser(description=__doc__)
arg_parser.add_argument('langs', nargs='?', default="eng",
                        help='languages passed to tesseract, eg. "eng+fra" (default: %(default)s)')
arg_parser.add_argument('-i', '--interval', type=int, default=None,
                        help='select a screen region then take textshots every INTERVAL milliseconds')


def take_textshot(langs, interval):

    QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
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

    window = QtWidgets.QMainWindow()
    if interval != None:
        snipper = IntervalSnipper(window, interval, langs)
        snipper.show()
    else:
        snipper = OneTimeSnipper(window, langs)
        snipper.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    args = arg_parser.parse_args()
    take_textshot(args.langs, args.interval)
