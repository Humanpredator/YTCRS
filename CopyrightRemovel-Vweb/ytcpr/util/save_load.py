import json
import os
from datetime import datetime

from ytcpr import FILE_DIR, LOGGER
from ytcpr.db.db_model import LogModel


def save_log(msg):
    log = LogModel()
    log.log_msg = msg
    log.log_created = datetime.now()
    log.save()
    LOGGER.info(msg)


async def load_session(email):
    SESSION_DATA = None
    try:
        session_file = os.path.join(FILE_DIR, f'{email}.json')
        with open(session_file, 'r') as f:
            SESSION_DATA = json.load(f)
        save_log(f"Fetching Cookies for {email}")
    except Exception:
        save_log(f'No Cookies Found for {email}')
    finally:
        return SESSION_DATA


async def save_session(email, data):
    SESSION_DATA = data
    try:
        session_file = os.path.join(FILE_DIR, f'{email}.json')
        with open(session_file, 'w') as f:
            json.dump(SESSION_DATA, f)
            save_log(f"Saving cookies for {email}")
    except Exception:
        save_log(f'Failed To Save cookies')
    finally:
        return SESSION_DATA
