from .messages import ocr_failure_message


def log_copied(copied):
    print(f'INFO: Copied "{copied}" to the clipboard')


def log_ocr_failure():
    """OCR didn't recognise text."""
    print_error(ocr_failure_message)


def log_ocr_error(error):
    """OCR produced an error."""
    print_error(error)


def print_error(error):
    print(f"ERROR: {error}")
