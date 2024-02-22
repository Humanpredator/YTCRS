import logging


# Create a custom encoding handler to handle non-ASCII characters
class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, encoding=None, mode='a', delay=False):
        if encoding is None:
            encoding = 'utf-8'  # Use UTF-8 encoding
        super().__init__(filename, mode, encoding, delay)


# Configure the logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)
