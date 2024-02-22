from typing import Optional

from studio.utils import get_nested_key


class Video:
    def __init__(self, video: dict):
        self._video = video
        self._video_id: Optional[str] = None
        self._channel_id: Optional[str] = None
        self._video_title: Optional[str] = None
        self._video_length: Optional[str] = None
        self._description: Optional[str] = None
        self._download_url: Optional[str] = None
        self._restriction: Optional[list] = None
        self._is_private: Optional[bool] = None
        self._is_drafted: bool = False
        self._edit_processing_status: Optional[str] = None
        self._video_status: Optional[str] = None
        self._insights: Optional[dict] = None
        self.__call__()

    def __call__(self, *args, **kwargs):
        if self._video:
            self._video_id = self._video.get('videoId')
            self._channel_id = self._video.get('channelId')
            self._video_title = self._video.get('title')
            self._video_length = self._video.get('lengthSeconds')
            self._description = self._video.get('description')
            self._download_url = self._video.get('downloadUrl')
            self._restriction = self._restriction_state(
                get_nested_key(self._video.get('allRestrictions'), 'reason'))
            self._is_private = self._video.get('privacy') == 'VIDEO_PRIVACY_PRIVATE'
            self._is_drafted = self._video.get('draftStatus') == 'DRAFT_STATUS_NONE'
            self._insights = {
                'total_comments': self._video.get('metrics').get('commentCount'),
                'total_dislike': self._video.get('metrics').get('dislikeCount'),
                'total_like': self._video.get('metrics').get('likeCount'),
                'total_view': self._video.get('metrics').get('viewCount')
            }
            self._edit_processing_status = self._edit_processing_state(self._video.get('inlineEditProcessingStatus'))
            self._video_status = self._video_state(self._video.get('status'))

        return self

    @staticmethod
    def _restriction_state(option: str):
        mapping = {
            "VIDEO_RESTRICTION_REASON_COPYRIGHT": "COPYRIGHT",
        }

        return mapping.get(option, "NO_RESTRICTION")

    @staticmethod
    def _edit_processing_state(option: str):
        mapping = {
            "VIDEO_PROCESSING_STATUS_EDITED": "EDITED",
            "VIDEO_PROCESSING_STATUS_UNEDITED": "UNEDITED",
            "VIDEO_PROCESSING_STATUS_PROCESSING": "PROCESSING",
        }

        return mapping.get(option, "UNKNOWN")

    @staticmethod
    def _video_state(option: str):
        mapping = {
            "VIDEO_STATUS_UPLOADED": "UPLOADED_CHECKING",
            "VIDEO_STATUS_PROCESSED": "PROCESSED",
        }

        return mapping.get(option, "UNKNOWN")

    @property
    def video_id(self) -> Optional[str]:
        return self._video_id

    @property
    def channel_id(self) -> Optional[str]:
        return self._channel_id

    @property
    def video_title(self) -> Optional[str]:
        return self._video_title

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def download_url(self) -> Optional[str]:
        return self._download_url

    @property
    def restriction(self) -> Optional[list]:
        return self._restriction

    @property
    def is_private(self) -> Optional[bool]:
        return self._is_private

    @property
    def is_drafted(self) -> bool:
        return self._is_drafted

    @property
    def insights(self) -> Optional[dict]:
        return self._insights

    @property
    def edit_processing_status(self) -> Optional[str]:
        return self._edit_processing_status

    @property
    def video_status(self) -> Optional[str]:
        return self._video_status

    @property
    def video_length(self) -> Optional[str]:
        return self._video_length
