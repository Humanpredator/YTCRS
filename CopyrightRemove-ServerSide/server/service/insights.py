from flask import render_template
from flask_mail import Message
from sqlalchemy import and_

from server import app, mail, executor, LOGGER
from server.config.cmn_func import datetime_india, add_scheduler
from server.database.db_model import SessionModel, VideoModel, ClaimModel


def fetch_all_session():
    dbsession = SessionModel.query.with_entities(
        SessionModel.pid,
        SessionModel.email_address,
        SessionModel.session_uid,
        SessionModel.state,
        SessionModel.ip_address,
        SessionModel.created_at).all()
    output = []
    for session in dbsession:
        videos = VideoModel.query.filter(VideoModel.session_pid == session.pid).all()
        session_output = {
            "total_videos": len(videos),
            "email": session.email_address,
            "ip": session.ip_address,
            "session_id": session.session_uid,
            "session_state": "Active" if session.state == 1 else "Inactive",
            "datetime": str(datetime_india()),
            "data": []
        }
        for video in videos:
            claims = ClaimModel.query.filter(
                and_(ClaimModel.video_pid == video.pid, ClaimModel.session_pid == session.pid)).all()
            video_claims = {
                "video_id": video.video_id,
                "video_title": video.video_title,
                "video_status": video.video_restrict,
                "video_checked_at": str(video.video_check_at),
                "total_claims": len(claims),
                "claims": [{
                    'claim_id': claim.claim_id,
                    'claim_title': claim.claim_title,
                    'claim_state': claim.claim_state,
                } for claim in claims]
            }
            session_output['data'].append(video_claims)
        output.append(session_output)
    return output


def send_email_async(subject, recipients, html_content):
    with app.app_context():
        message = Message(subject=subject, recipients=recipients, html=html_content)
        mail.send(message)


def send_report():
    with app.app_context():
        subject = 'YT Studio Report'
        for data in fetch_all_session():
            html_content = render_template('insights.html', data=data)
            recipients = [data['email']]
            executor.submit(send_email_async, subject, recipients, html_content)
        LOGGER.info('Email sending task started successfully!')


add_scheduler(send_report, interval=7200)
