import asyncio
import sys

from ytcpr import CHROME_PATH, USER_AGENT
from ytcpr.util.save_load import load_session, save_session, save_log


async def login(email, passwd, chromium):
    session_data = await load_session(email)
    if not session_data:
        browser = await chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled'
            ],
        )
        browser_context = await browser.new_context(user_agent=USER_AGENT, java_script_enabled=True)

        # LOG
        # save_log(f'No Cookies Found For {email},Trying To Login Using Given Creds.')
        # LOG
        # save_log(f'Opening The Browser In Head Mode...!')

        page = await browser_context.new_page()
        # LOG
        # save_log(f"Open Url: https://studio.youtube.com")
        await page.goto("https://studio.youtube.com")

        # Login Using Username And Password if user is not logged in
        if "accounts.google.com" in page.url.split('/'):

            # LOG
            save_log(f"Logging In...!")

            await page.fill('input[type="email"]', f"{email}")
            await page.click('div#identifierNext')

            await asyncio.sleep(5)
            await page.wait_for_selector('input[type="password"]', state="visible")
            await page.fill('input[type="password"]', f"{passwd}")
            await page.click('div#passwordNext')

            await asyncio.sleep(5)
            await page.wait_for_selector('[id="menu-paper-icon-item-1"]', state="attached")
            session_data = await browser_context.storage_state()
            await save_session(email, session_data)

            # LOG
            # save_log(f'Successfully Logged In, Session Saved on "{email}"')

            await browser_context.close()
            await browser.close()
        else:
            # LOG
            save_log(f"Unable To Login Try Again Later, Existing...!")
            sys.exit(1)
    return session_data
