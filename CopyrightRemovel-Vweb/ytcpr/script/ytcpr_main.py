import asyncio
import sys
from datetime import datetime

from playwright.async_api import Page
from sqlalchemy import and_

from ytcpr import WAIT_TIME, session, SESSION_ID
from ytcpr.db.db_model import VideoModel, SessionModel, VideoCheckModel, CRCSegmentModel, SegmentCheckModel, MetaData
from ytcpr.util.cont_fetcher import fetch_videos, fetch_claims_segment
from ytcpr.util.db_button import (
    clk_next_page, clk_first_page, cont_status, clk_see_detail, clk_rmv_clm_cont_mnu,
    slt_mute_song, mute_song_only, clk_seg_close_btn
)
from ytcpr.util.save_load import save_log


async def sleep_between_operations():
    await asyncio.sleep(0.5)


async def process_video(web_page, ytcr_session, vid_list, total_page, total_videos, total_claims, no_of_iter, page_no):
    videos = await fetch_videos(web_page, vid_list)
    save_log(f"Found:{len(videos)}, Page No: {page_no}")
    total_videos += len(videos)

    for idx, video in enumerate(videos, start=1):
        await sleep_between_operations()

        video_meta = video.locator('[id="video-title"]')
        video_title = str(await video_meta.text_content()).strip()
        video_id = (
            str(await video_meta.get_attribute('href')).split('/')[2]
            if await video_meta.get_attribute('href') else "NOT FOUND"
        )

        content_status, state = await cont_status(video)
        save_log(f"VideoName: {video_title}, VideoId: {video_id}, CopyRightStatus: {content_status}")

        video_detail = session.query(VideoModel).filter(
            and_(VideoModel.session_id == ytcr_session.session_id, VideoModel.video_title == video_title,
                 VideoModel.video_uid == video_id)).first()
        if not video_detail:
            video_detail = VideoModel()
        video_detail.session_id = ytcr_session.session_id
        video_detail.video_title = video_title
        video_detail.video_uid = video_id
        video_detail.video_last_check = datetime.now()

        vid = video_detail.save()
        video_status = VideoCheckModel()
        video_status.video_id = vid
        video_status.video_checked_count = no_of_iter
        video_status.video_checked_time = video_detail.video_last_check
        video_status.video_checked_status = content_status
        video_status.save()

        if not state:
            session.commit()
            continue
        await clk_see_detail(web_page)

        segments = await fetch_claims_segment(web_page)
        if not video_detail.video_int_claims:
            video_detail.video_int_claims = len(segments)
            video_detail.video_curr_claims = video_detail.video_int_claims
        else:
            video_detail.video_curr_claims = len(segments)
        session.commit()
        total_claims += len(segments)

        save_log(f"VideoName: {video_title}, VideoId: {video_id}, Claims:{len(segments)}")

        for ids, segment in enumerate(segments, start=1):
            await sleep_between_operations()

            segment_title = str(await segment.locator('[id="asset-title"]').text_content()).strip()
            segment_duration = str(await segment.locator(
                '[class="time-interval-button remove-default-style style-scope ytcr-video-content-list-claim-row"]').text_content()).strip()
            save_log(f"ClaimNo: {ids}, SegmentName: {segment_title}, SegmentDuration: {segment_duration}")

            seg_detail = session.query(CRCSegmentModel).filter(
                and_(CRCSegmentModel.video_id == vid,
                     CRCSegmentModel.segment_title == segment_title.strip())).first()
            if not seg_detail:
                seg_detail = CRCSegmentModel()
            seg_detail.segment_title = segment_title.strip()
            seg_detail.segment_impact = segment_duration
            seg_detail.video_id = vid
            seg_id = seg_detail.save()
            seg_check = SegmentCheckModel()
            seg_check.segment_id = seg_id
            seg_check.segment_checked_count = no_of_iter
            seg_check.segment_checked_time = datetime.now()
            seg_check.save()

            if not await clk_rmv_clm_cont_mnu(segment):
                session.commit()
                continue
            if await slt_mute_song(web_page):
                if await mute_song_only(web_page):
                    seg_check.segment_checked_status = "INITIATED FOR MUTE"
                    save_log(f"SegmentName: {segment_title}, ClaimStatus: INITIATED FOR MUTE")
                    session.commit()
                    break
                else:
                    seg_check.segment_checked_status = "MUTE SONG ONLY OPT UNAVAILABLE"
                    save_log(f"SegmentName: {segment_title}, ClaimStatus: MUTE SONG ONLY OPT UNAVAILABLE")
            else:
                seg_check.segment_checked_status = "MUTE SONG MENU UNAVAILABLE"
                save_log(f"SegmentName: {segment_title}, ClaimStatus: MUTE SONG MENU UNAVAILABLE")
            session.commit()
        await clk_seg_close_btn(web_page)

    return total_page, total_videos, total_claims, no_of_iter


async def execute(web_page: Page, vid_list):
    await web_page.goto('https://studio.youtube.com/')

    await web_page.click('[id="menu-paper-icon-item-1"]', timeout=10000)

    total_page = 1
    total_videos = 0
    total_claims = 0

    page_no = 1
    no_of_iter = 1

    ytcr_session = session.query(SessionModel).filter(SessionModel.session_uid == SESSION_ID).first()
    if not ytcr_session:
        save_log(f'Failed To Launch Your Session, Please Restart Again....')
        sys.exit(1)

    while True:
        total_page, total_videos, total_claims, no_of_iter = await process_video(
            web_page, ytcr_session, vid_list, total_page, total_videos, total_claims, no_of_iter, page_no
        )

        if not await clk_next_page(web_page):
            await clk_first_page(web_page)
            md = MetaData()
            md.session_id = ytcr_session.session_id
            md.total_page = total_page
            md.total_claims = total_claims
            md.total_video = total_videos
            md.iter_no = no_of_iter
            md.last_check = datetime.now()
            md.save()
            save_log(f"No More Pages Left Moving To First Page, Waiting Time: {WAIT_TIME}'s")
            no_of_iter += 1
            await web_page.reload()
            await asyncio.sleep(WAIT_TIME)
            page_no = 1
            total_page = 1
            total_videos = 0
            total_claims = 0
        else:
            save_log(f"Moving On Page: {page_no}")
            page_no += 1
            total_page += 1
