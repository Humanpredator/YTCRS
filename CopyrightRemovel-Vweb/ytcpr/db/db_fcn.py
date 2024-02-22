from datetime import datetime

from sqlalchemy import and_

from ytcpr import session
from ytcpr.db.db_model import SessionModel
from ytcpr.misc.cmn_fcn import get_current_ip


def create_session(email, sid):
    ins = session.query(SessionModel).filter(
        and_(SessionModel.session_uid == sid, SessionModel.email_address == email.strip())).first()
    if not ins:
        ins = SessionModel()
    ins.email_address = email
    ins.session_uid = sid
    ins.ip_address = get_current_ip()
    ins.created_at = datetime.now()
    session_id = ins.save()
    return session_id
