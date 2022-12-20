import pytesseract
from PIL import Image
import sys
import io
from .logger import log_ocr_error, print_error
from .notifications import notify
from PyQt5 import QtCore
from .messages import ocr_error_message


def ensure_tesseract_installed():
    try:
        pytesseract.get_tesseract_version()
    except EnvironmentError:
        notify(
            "Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        print_error(
            "Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        sys.exit()


def get_ocr_result(img, lang=None):
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_img = Image.open(io.BytesIO(buffer.data()))
    buffer.close()

    try:
        return pytesseract.image_to_string(pil_img, timeout=5, lang=lang).strip()
    except RuntimeError as error:
        log_ocr_error(error)
        notify(ocr_error_message(error))
        return
