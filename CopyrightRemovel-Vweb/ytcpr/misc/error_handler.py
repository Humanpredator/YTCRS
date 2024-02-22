from ytcpr import LOGGER


def exception_handler(exctype, value, traceback):
    LOGGER.critical(
        f"Error Occurred: {exctype.__name__}: {value}\nContact Support\nSession Existing...!")
