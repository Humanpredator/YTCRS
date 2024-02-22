import ctypes
import os
from dotenv import load_dotenv
load_dotenv('config.env')
from requests import Session

API_URL =os.getenv('API_URL')


def set_fullscreen():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 3)


set_fullscreen()

WAIT_TIME = 100

sessions = Session()
sessions.headers = {
    "Authorization": os.getenv('AUTHORIZATION')
}
