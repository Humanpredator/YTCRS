import os

from ytcr import sessions, API_URL
from ytcr.misc.cmn_fcn import get_current_ip


def create_session(email):
    url = API_URL + "request-session"
    payload = {
        "email": email,
        "ip": get_current_ip()
    }
    response = sessions.post(url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json().get('session_id')


def log_video(video_id, video_title, video_restrict):
    url = API_URL + "video"
    params = {
        "session_id": os.environ["SESSION_ID"]
    }
    payload = {
        "video_id": video_id,
        "video_title": video_title,
        "video_restriction": video_restrict

    }
    response = sessions.post(url, params=params, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def log_claim(video_id, claim_id, claim_title, claim_status,claim_state):
    url = API_URL + "claim"
    params = {
        "session_id": os.environ["SESSION_ID"],
        "video_id": video_id
    }
    payload = {
        "claim_id": claim_id,
        "claim_title": claim_title,
        "claim_status": claim_status,
        "claim_state":claim_state

    }
    response = sessions.post(url, params=params, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()
