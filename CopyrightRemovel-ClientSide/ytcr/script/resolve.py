import time

from studio import LOGGER, Studio

from ytcr import WAIT_TIME
from ytcr.db.db_fcn import log_video, log_claim


def resolve_claims(std: Studio, inc_video, exc_video):
    while True:
        videos = list(std.list_videos())
        if inc_video:
            videos = [video for video in videos if video.video_id in inc_video]
        if exc_video:
            videos = [video for video in videos if video.video_id not in inc_video]
        LOGGER.info(f"Total Number Of Videos Fetched: {len(videos)}")
        for ids, video in enumerate(videos, start=1):
            log_video(
                video.video_id,
                video.video_title,
                video.restriction
            )
            if video.restriction == "COPYRIGHT" and video.edit_processing_status != "PROCESSING":
                claims = list(std.list_video_claims(video))
                LOGGER.info(
                    f"Total Number Of Claims : {len(claims)} On VideoId {video.video_id}, VideoTitle: {video.video_title}")
                for claim in claims:

                    if "MUTE_SONG" not in claim.resolve_option:
                        log_claim(
                            claim.video_id,
                            claim.claim_id,
                            claim.claim_title,
                            claim.status,
                            claim_state="MUTE_SONG_ONLY_OPTION_UNAVAILABLE"
                        )
                        LOGGER.info("Mute Song Segment Unavailable...!")
                        continue
                    res = std.mute_segment_songs(claim)
                    if res_code := res.get('code') == "INITIATED_FOR_EDIT":
                        LOGGER.info(
                            f"VideoId: {claim.video_id}, ClaimId: {claim.claim_id}, ClaimTitle: {claim.claim_id}, Status: INITIATED FOR EDITING PROCESS")
                    else:
                        LOGGER.info(
                            f"ClaimId: {claim.claim_id}, ClaimTitle: {claim.claim_id}, Status: SEGMENT EDITING IN PROGRESS")
                    log_claim(
                        claim.video_id,
                        claim.claim_id,
                        claim.claim_title,
                        claim.status,
                        claim_state=res_code
                    )
            else:
                LOGGER.info(
                    f"VideoId:{video.video_id}, VideoTitle: {video.video_title}, Status: {video.restriction}, State:{video.edit_processing_status}")
        LOGGER.info(f"No More Content Available, Waiting Time: {WAIT_TIME}s")
        time.sleep(WAIT_TIME)
