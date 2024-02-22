from typing import Optional,  List

from studio.utils import get_nested_key


class Claims:
    def __init__(self, claim: dict):
        self._claim = claim
        self._claim_id: Optional[str] = None
        self._video_id: Optional[str] = None
        self._type: Optional[str] = None
        self._duration: Optional[str] = None
        self._resolve_option: Optional[List[str]] = None
        self._claim_title: Optional[str] = None
        self._status: Optional[str] = None
        self._artists: Optional[List[str]] = None
        self.__call__()

    def __call__(self, *args, **kwargs):
        self._claim_id = self._claim.get('claimId')
        self._video_id = self._claim.get('videoId')
        self._type = self._claim.get('type')

        start_time_seconds = int(self._claim.get("matchDetails", {}).get("longestMatchStartTimeSeconds", 0))
        duration_seconds = int(self._claim.get("matchDetails", {}).get("longestMatchDurationSeconds", 0))
        end_time_seconds = start_time_seconds + duration_seconds

        start_time_minutes, start_time_seconds = divmod(start_time_seconds, 60)
        end_time_minutes, end_time_seconds = divmod(end_time_seconds, 60)
        self._duration = f"{start_time_minutes:02d}:{start_time_seconds:02d} - {end_time_minutes:02d}:{end_time_seconds:02d}"

        self._resolve_option = self._available_option(self._claim.get('nontakedownClaimActions', {}).get('options'))

        meta_data = self._claim.get('asset', {}).get('srMetadata') or self._claim.get('asset', {}).get('metadata', {})
        self._claim_title = get_nested_key(meta_data, 'title')
        self._status = self._claim.get('status')
        self._artists = get_nested_key(meta_data, 'artists')

        return self

    @staticmethod
    def _available_option(options: list):
        mapping = {
            "NON_TAKEDOWN_CLAIM_OPTION_ERASE_SONG": "MUTE_SONG",
            "NON_TAKEDOWN_CLAIM_OPTION_TRIM": "TRIM_SEGMENT",
        }

        return [mapping.get(option, "UNAVAILABLE") for option in options if option in mapping] or ["UNAVAILABLE"]

    @property
    def claim_id(self) -> Optional[str]:
        return self._claim_id

    @property
    def video_id(self) -> Optional[str]:
        return self._video_id

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def duration(self) -> Optional[str]:
        return self._duration

    @property
    def resolve_option(self) -> Optional[List[str]]:
        return self._resolve_option

    @property
    def claim_title(self) -> Optional[str]:
        return self._claim_title

    @property
    def status(self) -> Optional[str]:
        return self._status

    @property
    def artists(self) -> Optional[List[str]]:
        return self._artists
