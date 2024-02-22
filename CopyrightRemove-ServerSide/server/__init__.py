import faulthandler
import logging
from concurrent.futures import ThreadPoolExecutor
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv('config.env')

faulthandler.enable()
class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, encoding=None, mode='a', delay=False):
        if encoding is None:
            encoding = 'utf-8'  # Use UTF-8 encoding
        super().__init__(filename, mode, encoding, delay)


# Configure the logging
logging.basicConfig(
    format=f"%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

app = Flask(__name__)

with app.app_context():
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    app.config["AUTHORIZATION"] = os.getenv('AUTHORIZATION')

    # Configuration for Flask-Mail with Google Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    mail = Mail(app)
    executor = ThreadPoolExecutor()
    db = SQLAlchemy(app)
    scheduler = BackgroundScheduler()
    # noinspection PyUnresolvedReferences
    from . import api, config, database, service

    scheduler.start()
    db.create_all()
