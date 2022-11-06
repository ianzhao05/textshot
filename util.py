import io

import pyperclip
import pytesseract
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from pynotifier import Notification
except ImportError:
    pass


def get_ocr_result(img, lang=None):
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_img = Image.open(io.BytesIO(buffer.data()))
    buffer.close()

    try:
        return pytesseract.image_to_string(
            pil_img, timeout=5, lang=lang
        ).strip()
    except RuntimeError as error:
        print(
            f"ERROR: An error occurred when trying to process the image: {error}")
        notify(f"An error occurred when trying to process the image: {error}")
        return


def send_ocr_result_to_clipboard(result):
    pyperclip.copy(result)


def print_copied(copied):
    print(f'INFO: Copied "{copied}" to the clipboard')


def notify_copied(copied):
    notify(f'Copied "{copied}" to the clipboard')


def notify(msg):
    try:
        Notification(title="TextShot", description=msg).send()
    except (SystemError, NameError):
        trayicon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(
                QtGui.QPixmap.fromImage(QtGui.QImage(
                    1, 1, QtGui.QImage.Format_Mono))
            )
        )
        trayicon.show()
        trayicon.showMessage("TextShot", msg, QtWidgets.QSystemTrayIcon.NoIcon)
        trayicon.hide()
