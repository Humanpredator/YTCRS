import asyncio


async def clk_seg_close_btn(page):
    try:
        close_button = page.locator('[class="close-button style-scope ytcr-video-home-dialog"]')
        if await close_button.is_enabled():
            await close_button.click()
            return 1
    except Exception:
        await page.keyboard.press('Escape')
        await asyncio.sleep(0.5)
    return None


async def mute_song_only(page):
    try:
        button_check = page.locator('[id="WAVE_FORM_ERASE"]')
        if await button_check.is_enabled() and not await button_check.is_checked():
            await button_check.check()

            continue_button = page.locator('[id="continue-button"]')
            if await continue_button.is_enabled():
                await continue_button.click()
            else:
                await page.keyboard.press('Escape')
                await asyncio.sleep(0.5)

            confirm_button = page.locator('[id="confirm-button"]')
            if await confirm_button.is_enabled():
                await confirm_button.click()
            else:
                await page.keyboard.press('Escape')
                await asyncio.sleep(0.5)
            return 1
        else:
            close_button = page.locator('[class="close-button style-scope ytcr-editing-tool-dialog"]')
            if await close_button.is_enabled():
                await close_button.click()
    except Exception:
        await page.keyboard.press('Escape')
        await asyncio.sleep(0.5)
    return None


async def slt_mute_song(page):
    try:
        paper_items = page.locator('tp-yt-paper-dialog:not([aria-hidden="true"])')
        mute_button = paper_items.locator('[test-id="NON_TAKEDOWN_CLAIM_OPTION_ERASE_SONG"]')
        if await mute_button.is_enabled():
            await mute_button.click()
            return 1
    except Exception:
        pass
    await page.keyboard.press('Escape')
    await asyncio.sleep(0.5)
    return None


async def clk_rmv_clm_cont_mnu(segment):
    try:
        action_button = segment.locator('[id="action-icon-button"]')
        if await action_button.is_enabled(timeout=1000):
            await action_button.click()
            return 1
    except Exception:
        pass
    return None


async def clk_see_detail(page):
    try:
        see_detail = page.locator(
            '[class="action-link style-scope ytcp-video-restrictions-tooltip-body"]',
            has_text="See details")
        await see_detail.click()
        return 1
    except Exception:
        pass
    return None


async def cont_status(video):
    is_cpr = None
    try:
        copyright_detail = video.locator('[id="restrictions-text"]')

        if str(cr_sts := await copyright_detail.text_content()) == 'Copyright':
            is_cpr = 1
            await copyright_detail.hover()
            await asyncio.sleep(2)
        return cr_sts, is_cpr
    except Exception:
        pass
    return None


async def clk_first_page(page):
    try:
        fp = page.locator('[id="navigate-first"]')
        if await fp.is_enabled():
            await fp.click()
            return 1
    except Exception:
        pass
    return None


async def clk_next_page(page):
    try:
        np = page.locator('[id="navigate-after"]')
        if await np.is_enabled():
            await np.click()
            return 1
    except Exception:
        pass
    return None
