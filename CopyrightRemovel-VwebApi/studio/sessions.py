import asyncio
import hashlib
import json
import os
import time
from typing import Optional
from contextlib import suppress

from playwright.sync_api import sync_playwright
from requests import Session

from studio.fh import FILE_DIR
from studio.logs import LOGGER


class AuthSession:
    def __init__(self,
                 email,
                 password,
                 chrome_path,
                 headless,
                 param_key,
                 user_agent):
        self._chrome_path = chrome_path
        self._headless = headless
        self._email: str = email
        self._session_path = os.path.join(FILE_DIR, f'{self._email}.json')
        self._password: str = password
        self.auth_key: str = param_key
        self._user_agent: str = user_agent
        self._session_token: str = Optional[str]
        self._channel_id: str = Optional[str]
        self.gauth_id = "0"

    def _header_cookies(self):
        required_cookie_field = ['__Secure-3PAPISID', '__Secure-3PSIDTS', '__Secure-3PSID']
        cookie_field = []
        sapid_value = None
        cd = self._load_session()
        for data in cd.get('cookies', []):
            if data['name'] in required_cookie_field:
                cookie_field.append(f"{data['name']}={data['value']}")
            if data['name'] == 'SAPISID':
                sapid_value = data['value']
        return "; ".join(set(cookie_field)), sapid_value

    def _load_session(self):
        with suppress(Exception):
            with open(self._session_path, 'r') as f:
                return json.load(f)
        return None

    def _save_session(self, data):
        with suppress(Exception):
            with open(self._session_path, 'w') as f:
                json.dump(data, f)

    @staticmethod
    async def _sapisid_hash(sapisid):
        origin = 'https://studio.youtube.com'
        timestamp_ms = int(time.time() * 1000)
        data_to_hash = f"{timestamp_ms} {sapisid} {origin}"
        encoded_str = data_to_hash.encode('utf-8')
        digest = await asyncio.to_thread(hashlib.sha1, encoded_str)
        return f"{timestamp_ms}_{digest.hexdigest()}"

    def _sessions(self) -> Session:
        self._cookie_session()
        default_session = Session()
        header_cookie, sapid_value = self._header_cookies()
        if not isinstance(header_cookie or sapid_value, str):
            raise ValueError('Failed To Get Valid Cookies')

        default_session.headers = {
            'authority': 'api.youtube.com',
            'authorization': f'SAPISIDHASH {asyncio.run(self._sapisid_hash(sapid_value))}',
            'studio-type': 'application/json',
            'cookie': header_cookie.strip(),
            'user-agent': self._user_agent,
            'x-goog-authuser': self.gauth_id,
            'x-origin': 'https://studio.youtube.com',

        }
        default_session.params = {
            'alt': "json",
            'key': self.auth_key
        }
        return default_session

    def _intercept_response(self, response):
        session_token_url = f'https://studio.youtube.com/youtubei/v1/ars/grst?alt=json&key={self.auth_key}'
        if session_token_url in response.url:
            data = response.json()
            self._session_token = data.get('sessionToken')

    def _cookie_session(self):
        LOGGER.info(f"Setting Up Session For {self._email}, Please Wait...!")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=self._chrome_path,
                headless=self._headless,
                args=['--disable-blink-features=AutomationControlled'],
            )
            session_data = self._load_session()
            browser_context = browser.new_context(storage_state=session_data, user_agent=self._user_agent,
                                                  java_script_enabled=True)
            page = browser_context.new_page()
            page.on("response", self._intercept_response)

            page.goto("https://studio.youtube.com")
            if "accounts.google.com" in page.url:
                LOGGER.info("Logging In With Given Credentials")
                page.fill('input[type="email"]', f"{self._email}")
                page.click('div#identifierNext')

                page.wait_for_selector('input[type="password"]', state="visible")
                page.fill('input[type="password"]', f"{self._password}")
                page.click('div#passwordNext')

                page.wait_for_selector('[id="menu-paper-icon-item-1"]', state="attached")
                session_data = browser_context.storage_state()
                self._save_session(session_data)
                LOGGER.info("Login Successfully...!")

            browser_context.storage_state = session_data
            LOGGER.info(f"Almost There Just Validating Session...!")
            page.wait_for_timeout(10000)
            self._channel_id = page.url.split('/')[-1]
            browser_context.close()

    def get_access_token(self, fresh=False):
        if fresh:
            self._cookie_session()
        return self._session_token
