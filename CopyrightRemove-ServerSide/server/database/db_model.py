# ----- This is related code -----
from sqlalchemy import Column, INTEGER, ForeignKey, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

from server import db


class SessionModel(db.Model):
    __tablename__ = 'session'

    pid = Column(INTEGER(), primary_key=True, autoincrement=True)
    email_address = Column(VARCHAR())
    session_uid = Column(VARCHAR(), unique=True)
    state = Column(INTEGER())  # 1-active, 0-Inactive
    ip_address = Column(VARCHAR())
    created_at = Column(TIMESTAMP())
    updated_at = Column(TIMESTAMP())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.pid


class VideoModel(db.Model):
    __tablename__ = 'video'

    pid = Column(INTEGER(), primary_key=True, autoincrement=True)
    video_title = Column(VARCHAR())
    video_id = Column(VARCHAR())
    video_restrict = Column(VARCHAR())
    video_check_at = Column(TIMESTAMP())
    # relationship
    session_pid = Column(INTEGER(), ForeignKey('session.pid', ondelete='SET NULL'))
    session_pid_fk = relationship("SessionModel", foreign_keys=[session_pid])

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.pid


class ClaimModel(db.Model):
    __tablename__ = 'claim'

    pid = Column(INTEGER(), primary_key=True, autoincrement=True)
    claim_id = Column(VARCHAR())
    claim_title = Column(VARCHAR())
    claim_status = Column(VARCHAR())
    claim_state = Column(VARCHAR())
    claim_checked_at = Column(TIMESTAMP())

    # relationship
    video_pid = Column(INTEGER(), ForeignKey('video.pid', ondelete='SET NULL'))
    video_pid_fk = relationship("VideoModel", foreign_keys=[video_pid])

    # relationship
    session_pid = Column(INTEGER(), ForeignKey('session.pid', ondelete='SET NULL'))
    session_pid_fk = relationship("SessionModel", foreign_keys=[session_pid])

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.pid
