# ----- This is related code -----
from sqlalchemy import Column, INTEGER, ForeignKey, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship

from ytcpr import Base, session


class LogModel(Base):
    __tablename__ = 'logs'

    log_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    log_msg = Column(VARCHAR())
    log_created = Column(TIMESTAMP())

    # relationship
    session_id = Column(INTEGER(), ForeignKey('session.session_id', ondelete='SET NULL'))
    session_id_fk = relationship("SessionModel", foreign_keys=[session_id])

    def save(self):
        session.add(self)
        session.commit()
        return self.log_id


class MetaData(Base):
    __tablename__ = 'meta_data'
    md_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    total_page = Column(INTEGER())
    total_video = Column(INTEGER())
    total_claims = Column(INTEGER())
    iter_no = Column(INTEGER())
    last_check = Column(TIMESTAMP())
    # relationship
    session_id = Column(INTEGER(), ForeignKey('session.session_id', ondelete='SET NULL'))
    session_id_fk = relationship("SessionModel", foreign_keys=[session_id])

    def save(self):
        session.add(self)
        session.commit()
        return self.md_id


class SessionModel(Base):
    __tablename__ = 'session'

    session_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    email_address = Column(VARCHAR())
    session_uid = Column(VARCHAR())
    ip_address = Column(VARCHAR())
    created_at = Column(TIMESTAMP())

    def save(self):
        session.add(self)
        session.flush()
        return self.session_id


class VideoModel(Base):
    __tablename__ = 'channel_videos'

    video_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    video_title = Column(VARCHAR())
    video_uid = Column(VARCHAR())
    video_int_claims = Column(INTEGER())
    video_curr_claims = Column(INTEGER())
    video_last_check = Column(TIMESTAMP())
    # relationship
    session_id = Column(INTEGER(), ForeignKey('session.session_id', ondelete='SET NULL'))
    session_id_fk = relationship("SessionModel", foreign_keys=[session_id])

    def save(self):
        session.add(self)
        session.flush()
        return self.video_id


class VideoCheckModel(Base):
    __tablename__ = 'video_check'
    video_check_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    video_checked_count = Column(INTEGER())
    video_checked_status = Column(VARCHAR())
    video_checked_time = Column(TIMESTAMP())

    # relationship
    video_id = Column(INTEGER(), ForeignKey('channel_videos.video_id', ondelete='SET NULL'))
    video_id_fk = relationship("VideoModel", foreign_keys=[video_id])

    def save(self):
        session.add(self)
        session.flush()
        return self.video_check_id


class CRCSegmentModel(Base):
    __tablename__ = 'crc_segment'

    segment_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    segment_title = Column(VARCHAR())
    segment_impact = Column(VARCHAR())

    # relationship
    video_id = Column(INTEGER(), ForeignKey('channel_videos.video_id', ondelete='SET NULL'))
    video_id_fk = relationship("VideoModel", foreign_keys=[video_id])

    def save(self):
        session.add(self)
        session.flush()
        return self.segment_id


class SegmentCheckModel(Base):
    __tablename__ = 'segment_check'
    segment_check_id = Column(INTEGER(), primary_key=True, autoincrement=True)
    segment_checked_status = Column(VARCHAR())
    segment_checked_count = Column(INTEGER())
    segment_checked_time = Column(TIMESTAMP())

    # relationship
    segment_id = Column(INTEGER(), ForeignKey('crc_segment.segment_id', ondelete='SET NULL'))
    segment_id_fk = relationship("CRCSegmentModel", foreign_keys=[segment_id])

    def save(self):
        session.add(self)
        session.flush()
        return self.segment_check_id
