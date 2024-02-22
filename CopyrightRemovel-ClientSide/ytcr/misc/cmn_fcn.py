import socket
import time
from functools import wraps

import requests
from studio import LOGGER


def get_current_ip():
    try:
        # Connect to a well-known service that echoes the client's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google's DNS server, port 80
        public_ip = s.getsockname()[0]
        s.close()
        return public_ip
    except:
        return 'NOT FOUND'


def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    response = func(*args, **kwargs)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    return response
                except requests.exceptions.RequestException as e:
                    LOGGER.error(f"Request failed: {e}")
                    retries += 1
                    if retries < max_retries:
                        LOGGER.error(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            LOGGER.error(f"Max retries reached. Giving up.")
            raise requests.exceptions.RetryError

        return wrapper

    return decorator
