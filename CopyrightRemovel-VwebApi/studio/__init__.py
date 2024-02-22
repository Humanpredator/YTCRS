import faulthandler
from collections.abc import Generator
from typing import Optional

from studio.claims import Claims
from studio.logs import LOGGER
from studio.sessions import AuthSession
from studio.utils import format_ms_to_time
from studio.videos import Video

faulthandler.enable()


class Studio(AuthSession):

    def __init__(self,
                 email: str,
                 password: str,
                 chrome_path: str = "C:\Program Files\Google\Chrome\Application\chrome.exe",
                 headless: bool = True,
                 param_key: str = "AIzaSyBUPetSUmoZL-OhlxA7wSac5XinrygCqMo",
                 user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'):
        super().__init__(email, password, chrome_path, headless, param_key, user_agent)
        self._session = self._sessions()
        self._base_url = "https://studio.youtube.com"
        self._version = "v1"
        self._service = "youtubei"

    def list_videos(self) -> Optional[Generator[Video, None, None]]:
        payload = {
            "filter": {
                "and": {
                    "operands": [
                        {
                            "channelIdIs": {
                                "value": self._channel_id
                            }
                        },
                        {
                            "and": {
                                "operands": [
                                    {
                                        "videoOriginIs": {
                                            "value": "VIDEO_ORIGIN_UPLOAD"
                                        }
                                    },
                                    {
                                        "not": {
                                            "operand": {
                                                "or": {
                                                    "operands": [
                                                        {
                                                            "contentTypeIs": {
                                                                "value": "CREATOR_CONTENT_TYPE_SHORTS"
                                                            }
                                                        },
                                                        {
                                                            "and": {
                                                                "operands": [
                                                                    {
                                                                        "not": {
                                                                            "operand": {
                                                                                "statusIs": {
                                                                                    "value": "VIDEO_STATUS_PROCESSED"
                                                                                }
                                                                            }
                                                                        }
                                                                    },
                                                                    {
                                                                        "isShortsEligible": {}
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            "order": "VIDEO_ORDER_DISPLAY_TIME_DESC",
            "pageSize": 30,
            "mask": {
                "channelId": True,
                "videoId": True,
                "lengthSeconds": True,
                "livestream": {
                    "all": True
                },
                "publicLivestream": {
                    "all": True
                },
                "origin": True,
                "premiere": {
                    "all": True
                },
                "publicPremiere": {
                    "all": True
                },
                "status": True,
                "thumbnailDetails": {
                    "all": True
                },
                "title": True,
                "draftStatus": True,
                "downloadUrl": True,
                "watchUrl": True,
                "shareUrl": True,
                "permissions": {
                    "all": True
                },
                "features": {
                    "all": True
                },
                "timeCreatedSeconds": True,
                "timePublishedSeconds": True,
                "privacy": True,
                "contentOwnershipModelSettings": {
                    "all": True
                },
                "contentType": True,
                "publicShorts": {
                    "all": True
                },
                "podcastRssMetadata": {
                    "all": True
                },
                "videoLinkageShortsAttribution": {
                    "all": True
                },
                "responseStatus": {
                    "all": True
                },
                "statusDetails": {
                    "all": True
                },
                "description": True,
                "metrics": {
                    "all": True
                },
                "thumbnailEditorState": {
                    "all": True
                },
                "titleFormattedString": {
                    "all": True
                },
                "descriptionFormattedString": {
                    "all": True
                },
                "titleDetails": {
                    "all": True
                },
                "descriptionDetails": {
                    "all": True
                },
                "audienceRestriction": {
                    "all": True
                },
                "releaseInfo": {
                    "all": True
                },
                "allRestrictions": {
                    "all": True
                },
                "inlineEditProcessingStatus": True,
                "videoPrechecks": {
                    "all": True
                },
                "shorts": {
                    "all": True
                },
                "selfCertification": {
                    "all": True
                },
                "videoResolutions": {
                    "all": True
                },
                "scheduledPublishingDetails": {
                    "all": True
                },
                "visibility": {
                    "all": True
                },
                "privateShare": {
                    "all": True
                },
                "sponsorsOnly": {
                    "all": True
                },
                "unlistedExpired": True,
                "videoTrailers": {
                    "all": True
                },
                "remix": {
                    "isSource": True
                },
                "isPaygated": True
            },
            "context": {
                "client": {
                    "clientName": 62,
                    "clientVersion": "1.20231122.03.00",
                    "hl": "en",
                    "gl": "IN",
                    "experimentsToken": "",
                    "utcOffsetMinutes": 330,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "screenWidthPoints": 1366,
                    "screenHeightPoints": 157,
                    "screenPixelDensity": 1,
                    "screenDensityFloat": 1
                },
                "request": {
                    "returnLogEntry": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": []
                }

            }
        }
        _url = f"{self._base_url}/{self._service}/{self._version}/creator/list_creator_videos"
        all_set = True
        while all_set:
            response = self._session.post(_url, json=payload)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 402:
                LOGGER.info("Google Session Expired, Trying Again Please Wait...!")
                self._session = self._sessions()
                return self.list_videos()
            if page_token := data.get('nextPageToken'):
                payload['pageToken'] = page_token
            else:
                all_set = False
            content_videos = data.get('videos', [])
            for ids, video_data in enumerate(content_videos, start=1):
                yield Video(video_data)

    def list_video_claims(self, video: Video) -> Optional[Generator[Claims, None, None]]:
        payload = {
            "context": {
                "client": {
                    "clientName": 62,
                    "clientVersion": "1.20231122.03.00",
                    "hl": "en",
                    "gl": "IN",
                    "experimentsToken": "",
                    "utcOffsetMinutes": 330,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "screenWidthPoints": 1366,
                    "screenHeightPoints": 342,
                    "screenPixelDensity": 1,
                    "screenDensityFloat": 1
                },
                "request": {
                    "returnLogEntry": True,
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": []
                },
                "user": {
                    "delegationContext": {
                        "externalChannelId": self._channel_id,
                        "roleType": {
                            "channelRoleType": "CREATOR_CHANNEL_ROLE_TYPE_OWNER"
                        }
                    }
                }
            },
            "videoId": video.video_id,
            "criticalRead": False,
            "includeLicensingOptions": False
        }
        _url = f"{self._base_url}/{self._service}/{self._version}/creator/list_creator_received_claims?alt=json&key={self.auth_key}"

        response = self._session.post(_url, json=payload)
        response.raise_for_status()
        if response.status_code == 402:
            LOGGER.info("Google Session Expired, Trying Again Please Wait...!")
            self._session = self._sessions()
            return self.list_video_claims(video)
        data = response.json().get('receivedClaims', [])

        for ids, claim in enumerate(data, start=1):
            yield Claims(claim)

    def _get_claimed_duration(self, claim: Claims):
        _url = f"{self._base_url}/{self._service}/{self._version}/copyright/get_creator_received_claim_matches"

        payload = {
            "videoId": claim.video_id,
            "claimId": claim.claim_id,
            "channelId": self._channel_id,
            "context": {
                "client": {
                    "clientName": 62,
                    "clientVersion": "1.20231128.04.00",
                    "hl": "en",
                    "gl": "IN",
                    "experimentsToken": "",
                    "utcOffsetMinutes": 330,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "screenWidthPoints": 811,
                    "screenHeightPoints": 629,
                    "screenPixelDensity": 1,
                    "screenDensityFloat": 1
                },
                "request": {
                    "returnLogEntry": True,
                    "internalExperimentFlags": []
                },
                "user": {
                    "delegationContext": {
                        "externalChannelId": self._channel_id,
                        "roleType": {
                            "channelRoleType": "CREATOR_CHANNEL_ROLE_TYPE_OWNER"
                        }
                    }
                }
            }
        }

        response = self._session.post(_url, json=payload)
        response.raise_for_status()
        if response.status_code == 402:
            LOGGER.info("Google Session Expired, Trying Again Please Wait...!")
            self._session = self._sessions()
            return self._get_claimed_duration(claim)
        res_data = response.json()
        claim_matches = res_data.get('matches').get('claimMatches')
        data = []
        for item in claim_matches:
            data.append(item.get('videoSegment'))
        return data

    def trim_out(self, claim: Claims):

        _url = f"{self._base_url}/{self._service}/{self._version}/video_editor/edit_video"

        payload = {
            "externalVideoId": claim.video_id,
            "claimEditChange": {
                "addRemoveSongEdit": {
                    "claimId": claim.claim_id,
                    "method": "REMOVE_SONG_METHOD_TRIM",
                    "muteSegments": self._get_claimed_duration(claim),
                    "allKnownMatchesCovered": False
                }
            },
            "context": {
                "client": {
                    "clientName": 62,
                    "clientVersion": "1.20231128.04.00",
                    "hl": "en",
                    "gl": "IN",
                    "experimentsToken": "",
                    "utcOffsetMinutes": 330,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "screenWidthPoints": 811,
                    "screenHeightPoints": 629,
                    "screenPixelDensity": 1,
                    "screenDensityFloat": 1
                },
                "request": {
                    "returnLogEntry": True,
                    "internalExperimentFlags": [],
                    "sessionInfo": {
                        "token": self.get_access_token()
                    },
                    "consistencyTokenJars": []
                },
                "user": {
                    "delegationContext": {
                        "externalChannelId": self._channel_id,
                        "roleType": {
                            "channelRoleType": "CREATOR_CHANNEL_ROLE_TYPE_OWNER"
                        }
                    }
                }
            }
        }

        response = self._session.post(_url, json=payload)
        if response.status_code == 409:
            return {
                'status': 'wait till existing edit process to complete...!',
                'code': "WAITING_FOR_COMPLETE"
            }
        if response.status_code == 402:
            LOGGER.info("Google Session Expired, Trying Again Please Wait...!")
            self._session = self._sessions()
            return self.trim_out(claim)
        response.raise_for_status()
        res_data = response.json()
        return {
            'status': res_data.get('executionStatus'),
            'code': "INITIATED_FOR_EDIT"
        }

    def mute_segment_songs(self, claim: Claims, song_only=True):

        _url = f"{self._base_url}/{self._service}/{self._version}/video_editor/edit_video"

        payload = {
            "externalVideoId": claim.video_id,
            "claimEditChange": {
                "addRemoveSongEdit": {
                    "claimId": claim.claim_id,
                    "method": "REMOVE_SONG_METHOD_WAVEFORM_ERASE" if song_only else "REMOVE_SONG_METHOD_MUTE",
                    "muteSegments": self._get_claimed_duration(claim),
                    "allKnownMatchesCovered": True
                }
            },
            "context": {
                "client": {
                    "clientName": 62,
                    "clientVersion": "1.20231128.04.00",
                    "hl": "en",
                    "gl": "IN",
                    "experimentsToken": "",
                    "utcOffsetMinutes": 330,
                    "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                    "screenWidthPoints": 811,
                    "screenHeightPoints": 629,
                    "screenPixelDensity": 1,
                    "screenDensityFloat": 1
                },
                "request": {
                    "returnLogEntry": True,
                    "internalExperimentFlags": [],

                    "sessionInfo": {
                        "token": self.get_access_token()
                    },
                    "consistencyTokenJars": []
                },
                "user": {
                    "delegationContext": {
                        "externalChannelId": self._channel_id,
                        "roleType": {
                            "channelRoleType": "CREATOR_CHANNEL_ROLE_TYPE_OWNER"
                        }
                    }
                }
            }
        }

        response = self._session.post(_url, json=payload)
        if response.status_code == 409:
            return {
                'status': 'wait until existing edit process to complete...!',
                'code': "WAITING_FOR_COMPLETE"
            }
        if response.status_code == 402:
            LOGGER.info("Google Session Expired, Trying Again Please Wait...!")
            self._session = self._sessions()
            return self.mute_segment_songs(claim, song_only)

        response.raise_for_status()
        res_data = response.json()
        return {
            'status': res_data.get('executionStatus'),
            'code': "INITIATED_FOR_EDIT"
        }
