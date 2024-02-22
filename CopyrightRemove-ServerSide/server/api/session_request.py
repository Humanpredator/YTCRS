import uuid

from flask import request, jsonify
from sqlalchemy import and_

from server import app
from server.config.cmn_func import datetime_india
from server.database.db_model import SessionModel, VideoModel, ClaimModel


@app.route("/request-session", methods=['POST'])
def request_session():
    data = request.json
    session = SessionModel()
    session.email_address = data['email']
    session.ip_address = data['ip']
    session.state = 1
    session.session_uid = str(uuid.uuid4())
    session.created_at = datetime_india()
    session.save()
    return jsonify(session_id=session.session_uid), 200


@app.route("/session-exception", methods=['POST'])
def session_exception():
    session_id = request.args['session_id']
    db_session = SessionModel.query.filter(SessionModel.session_uid == session_id).first()
    if not db_session:
        return jsonify(error="No Session Found"), 400
    db_session.state = 0
    db_session.updated_at = datetime_india()
    db_session.save()
    return jsonify(error="Session Terminated Due To Unexpected Error...!"), 200


@app.route("/video", methods=['POST'])
def inbound_videos():
    data = request.json
    session_id = request.args['session_id']

    db_session = SessionModel.query.filter(SessionModel.session_uid == session_id).first()
    if not db_session:
        return jsonify(error="No Session Found"), 400

    videos = VideoModel.query.filter(and_(
        VideoModel.video_id == data['video_id'], VideoModel.session_pid == db_session.pid
    )).first()
    if not videos:
        videos = VideoModel()

    videos.video_id = data['video_id']
    videos.video_title = data['video_title']
    videos.session_pid = db_session.pid
    videos.video_restrict = data['video_restriction']
    videos.video_check_at = datetime_india()
    videos.save()

    return jsonify(video_id=videos.video_id), 200


@app.route("/claim", methods=['POST'])
def inbound_claims():
    data = request.json
    session_id = request.args['session_id']
    video_id = request.args['video_id']

    db_session = SessionModel.query.filter(SessionModel.session_uid == session_id).first()
    if not db_session:
        return jsonify(error="No Session Found"), 400

    videos = VideoModel.query.filter(and_(
        VideoModel.video_id == video_id, VideoModel.session_pid == db_session.pid
    )).first()
    if not videos:
        return jsonify(error="No VideoId Found"), 400

    claim = ClaimModel.query.filter(and_(
        ClaimModel.video_pid == videos.pid, ClaimModel.session_pid == db_session.pid
    )).first()
    if not claim:
        claim = ClaimModel()

    claim.session_pid = db_session.pid
    claim.video_pid = videos.pid
    claim.claim_id = data["claim_id"]
    claim.claim_title = data["claim_title"]
    claim.claim_status = data["claim_status"]
    claim.claim_state = data['claim_state']
    claim.claim_checked_at = datetime_india()
    claim.save()
    return jsonify(claim_id=claim.claim_id), 200
