import sys

from playwright.async_api import async_playwright, Playwright

from ytcpr import SESSION_ID, HEADLESS, CHROME_PATH, USER_AGENT
from ytcpr.db.db_fcn import create_session
from ytcpr.misc.error_handler import exception_handler
from ytcpr.script.yt_login import login
from ytcpr.script.ytcpr_main import execute
from ytcpr.util.save_load import save_log

sys.excepthook = exception_handler


async def open_new_page(playwright: Playwright, email, password):
    chromium = playwright.chromium  # or "firefox" or "webkit".

    session_data = await login(email, password, chromium)
    browser = await chromium.launch(
        executable_path=CHROME_PATH,
        headless=HEADLESS,
        args=[
            '--disable-blink-features=AutomationControlled'
        ],
    )
    browser_context = await browser.new_context(storage_state=session_data,
                                                user_agent=USER_AGENT,
                                                java_script_enabled=True
                                                )
    #
    # save_log(f'Opening The Browser In Headless Mode...!')

    new_page = await browser_context.new_page()
    return new_page


async def run_ytcpr(email, password, video_id):
    async with async_playwright() as playwright:
        page = await open_new_page(playwright, email, password)
        save_log(f"Launching Session, Please Wait")
        create_session(email, SESSION_ID)
        await execute(page, video_id)
