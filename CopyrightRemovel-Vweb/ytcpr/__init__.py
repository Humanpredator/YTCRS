import faulthandler
import logging
import os
import sys
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv('config.env')

faulthandler.enable()
SESSION_ID = str(uuid.uuid4())[:10]


# Create a custom encoding handler to handle non-ASCII characters
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

FILE_DIR = os.path.join(os.getcwd(), '.temp')
os.makedirs(FILE_DIR, exist_ok=True)

CHROME_PATH =os.getenv('CHROME_PATH')
HEADLESS = True
USER_AGENT = os.getenv('USER_AGENT')
WAIT_TIME = 100

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
try:

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
except:
    LOGGER.error('Failed to Connect To The DB Server, Existing...!')
    sys.exit(1)

from . import db

Base.metadata.create_all(engine)
