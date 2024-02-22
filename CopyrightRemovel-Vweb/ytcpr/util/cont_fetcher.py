async def fetch_claims_segment(page):
    try:
        await page.wait_for_selector('div.content-row-container.style-scope.ytcr-video-content-list',
                                     state="visible")
        segments = await page.locator('div.content-row-container.style-scope.ytcr-video-content-list').all()
        return segments
    except Exception:
        pass
    return None


async def fetch_videos(page, vid_list):
    try:
        await page.wait_for_selector('[id="row-container"]')
        videos = await page.locator('[id="row-container"]').all()
        if not vid_list:
            return videos

        video_list = []
        for video in videos:
            video_meta = video.locator('[id="video-title"]')
            video_id = str(await video_meta.get_attribute('href')).split('/')[
                2] if await video_meta.get_attribute('href') else "VIDEO ID NOT FOUND"
            if video_id in vid_list:
                video_list.append(video)
        return video_list

    except Exception:
        pass
    return []
