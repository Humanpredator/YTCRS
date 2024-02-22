import os
import sys
import time

from studio import LOGGER, Studio

from ytcr import API_URL, sessions
from ytcr.db.db_fcn import create_session
from ytcr.script.resolve import resolve_claims


def exception_handler(exctype, value, traceback):
    url = API_URL + "/session-exception"
    params = {
        "session_id": os.environ["SESSION_ID"]
    }
    sessions.post(url, params=params)
    LOGGER.critical(
        f"Error Occurred: {exctype.__name__}: {value}\nContact Support\nSession Existing...!")
    time.sleep(10)


sys.excepthook = exception_handler


def run(email, password, inc_video, exc_video):
    std = Studio(email, password)
    os.environ["SESSION_ID"] = create_session(email)
    if not os.environ["SESSION_ID"]:
        LOGGER.info(f"Unable to Connect to the Server, Please Try Again...!")
    resolve_claims(std, inc_video, exc_video)
