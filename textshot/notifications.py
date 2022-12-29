from PyQt5 import QtGui, QtWidgets

from .messages import ocr_failure_message

try:
    from pynotifier import Notification
except ImportError:
    pass


def notify_ocr_failure():
    notify(ocr_failure_message)


def notify_copied(copied):
    notify(f'Copied "{copied}" to the clipboard')


def notify(msg):
    try:
        Notification(title="TextShot", description=msg).send()
    except (SystemError, NameError):
        trayicon = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(
                QtGui.QPixmap.fromImage(QtGui.QImage(1, 1, QtGui.QImage.Format_Mono))
            )
        )
        trayicon.show()
        trayicon.showMessage("TextShot", msg, QtWidgets.QSystemTrayIcon.NoIcon)
        trayicon.hide()
