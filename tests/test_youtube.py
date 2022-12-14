"""Module containing tests for the youtube service"""
import time
from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call

from services import create_app
from services.youtube.dtos import SubscriptionListResponse, ChannelDetails, PlaylistItemListResponse
from utils.testing import MockResponse

_app = create_app(config_filename="test.config.json", should_log_err_to_file=False)


class TestYoutube(TestCase):
    """Tests for the YouTube service"""

    def setUp(self) -> None:
        """Initialize a few common variables"""
        self.client = _app.test_client()

    @patch("requests.get")
    def test_get_subscriptions(self, mock_get: MagicMock):
        """Should return the SubscriptionListResponse response after querying the YouTube data v3 endpoint"""
        access_token = "some dummy stuff-1"
        mock_response = {
            "kind": "youtube#SubscriptionListResponse",
            "etag": "Oqgkyuuyyb",
            "nextPageToken": "yutth",
            "pageInfo": {
                "totalResults": 39,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#subscription",
                    "etag": "iuyyuy",
                    "id": "iuyuvghkg",
                    "snippet": {
                        "publishedAt": "2022-07-12T21:05:09.560563Z",
                        "title": "Yoooo",
                        "description": "Some stuff",
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": "iuiuoaiuh"
                        },
                        "channelId": "ayueuwtwtehgj",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/kk"
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/uueh"
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/yteh"
                            }
                        }
                    }
                },
                {
                    "kind": "youtube#subscription",
                    "etag": "ayuadsa",
                    "id": "aiow78237832bkja",
                    "snippet": {
                        "publishedAt": "2019-08-29T22:27:02.940163Z",
                        "title": "Penicilin",
                        "description": "",
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": "Gundi"
                        },
                        "channelId": "Gigabipwe7983",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/ye7"
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/yutew"
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/uyyere"
                            }
                        }
                    }
                },
            ],
        }
        expected_response = SubscriptionListResponse(**mock_response).dict(exclude_unset=True)
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_url = "https://youtube.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=mock_response, status_code=200)

        response = self.client.get("/youtube/subscriptions", headers={"X-YouHedge-Token": access_token})
        mock_get.assert_called_with(expected_url, headers=expected_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response, response.json)

    @patch("requests.get")
    def test_cached_get_subscriptions(self, mock_get: MagicMock):
        """Should return the cached response as long as TTL is not exceeded"""
        access_token = "some dummy stuff-2"
        other_access_token = "wooohooo"
        first_mock_response = {
            "kind": "youtube#SubscriptionListResponse",
            "etag": "Oqgkyuuyyb",
            "nextPageToken": "yutth",
            "pageInfo": {
                "totalResults": 39,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#subscription",
                    "etag": "iuyyuy",
                    "id": "iuyuvghkg",
                    "snippet": {
                        "publishedAt": "2022-07-12T21:05:09.560563Z",
                        "title": "Yoooo",
                        "description": "Some stuff",
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": "iuiuoaiuh"
                        },
                        "channelId": "ayueuwtwtehgj",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/kk"
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/uueh"
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/yteh"
                            }
                        }
                    }
                },
            ],
        }
        second_mock_response = {
            "kind": "youtube#SubscriptionListResponse",
            "etag": "jksjds",
            "nextPageToken": "tywtew",
            "pageInfo": {
                "totalResults": 60,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#subscription",
                    "etag": "ayuadsa",
                    "id": "aiow78237832bkja",
                    "snippet": {
                        "publishedAt": "2019-08-29T22:27:02.940163Z",
                        "title": "Penicilin",
                        "description": "",
                        "resourceId": {
                            "kind": "youtube#channel",
                            "channelId": "Gundi"
                        },
                        "channelId": "Gigabipwe7983",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/ye7"
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/yutew"
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/uyyere"
                            }
                        }
                    }
                },
            ],
        }
        expected_old_response = SubscriptionListResponse(**first_mock_response).dict(exclude_unset=True)
        expected_updated_response = SubscriptionListResponse(**second_mock_response).dict(exclude_unset=True)
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        other_headers = {"Accept": "application/json", "Authorization": f"Bearer {other_access_token}"}
        expected_url = "https://youtube.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=first_mock_response, status_code=200)
        self.client.get("/youtube/subscriptions", headers={"X-YouHedge-Token": access_token})

        # change the mock response
        mock_get.return_value = MockResponse(data=second_mock_response, status_code=200)

        # change headers and thus skip the cache
        new_headers_response = self.client.get("/youtube/subscriptions",
                                               headers={"X-YouHedge-Token": other_access_token})

        # use old headers and thus hit the cache
        old_headers_response = self.client.get("/youtube/subscriptions", headers={"X-YouHedge-Token": access_token})

        # wait for TTL to elapse and try the query again
        time.sleep(3)
        old_headers_after_sleep_response = self.client.get("/youtube/subscriptions",
                                                           headers={"X-YouHedge-Token": access_token})

        calls = [
            call(expected_url, headers=expected_headers),
            call(expected_url, headers=other_headers),
            call(expected_url, headers=expected_headers),
        ]
        mock_get.assert_has_calls(calls=calls)
        self.assertEqual(200, old_headers_response.status_code)
        self.assertEqual(200, new_headers_response.status_code)
        self.assertEqual(200, old_headers_after_sleep_response.status_code)
        self.assertEqual(expected_updated_response, new_headers_response.json)
        self.assertEqual(expected_old_response, old_headers_response.json)
        self.assertEqual(expected_updated_response, old_headers_after_sleep_response.json)

    @patch("requests.get")
    def test_get_channel_details(self, mock_get: MagicMock):
        """Should return the ChannelDetailsResponse response after querying the YouTube data v3 endpoint"""
        access_token = "some dummy stuff-1"
        channel_id = "a random channel id"
        mock_response = {
            "kind": "youtube#channelListResponse",
            "etag": "syudsabka",
            "pageInfo": {
                "totalResults": 1,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#channel",
                    "etag": "ayuahkjhada",
                    "id": "a random channel id",
                    "snippet": {
                        "title": "Yoooo Mahn",
                        "description": "",
                        "publishedAt": "2018-03-07T12:17:06Z",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/gha",
                                "width": 88,
                                "height": 88
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/ayu",
                                "width": 240,
                                "height": 240
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/ryt",
                                "width": 800,
                                "height": 800
                            }
                        },
                        "localized": {
                            "title": "Yooo Mahn",
                            "description": ""
                        }
                    },
                    "contentDetails": {
                        "relatedPlaylists": {
                            "likes": "",
                            "uploads": "eyuryejhhrje"
                        }
                    }
                }
            ]
        }
        expected_response = ChannelDetails(**mock_response["items"][0]).dict(exclude_unset=True)
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={channel_id}&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=mock_response, status_code=200)

        response = self.client.get(f"/youtube/channels/{channel_id}", headers={"X-YouHedge-Token": access_token})
        mock_get.assert_called_with(expected_url, headers=expected_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response, response.json)

    @patch("requests.get")
    def test_cached_get_channel_details(self, mock_get: MagicMock):
        """Should return the cached ChannelDetailsResponse response for the given request if TTL is not yet exceeded."""
        access_token = "some dummy stuff-2"
        other_access_token = "wooohooo"
        channel_id = "a random channel id"
        other_channel_id = "a random chaner id"
        first_mock_response = {
            "kind": "youtube#channelListResponse",
            "etag": "syudsabka",
            "pageInfo": {
                "totalResults": 1,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#channel",
                    "etag": "ayuahkjhada",
                    "id": "a random channel id",
                    "snippet": {
                        "title": "Yoooo Mahn",
                        "description": "",
                        "publishedAt": "2018-03-07T12:17:06Z",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/gha",
                                "width": 88,
                                "height": 88
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/ayu",
                                "width": 240,
                                "height": 240
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/ryt",
                                "width": 800,
                                "height": 800
                            }
                        },
                        "localized": {
                            "title": "Yooo Mahn",
                            "description": ""
                        }
                    },
                    "contentDetails": {
                        "relatedPlaylists": {
                            "likes": "",
                            "uploads": "eyuryejhhrje"
                        }
                    }
                }
            ]
        }
        second_mock_response = {
            "kind": "youtube#channelListResponse",
            "etag": "ajkhda",
            "pageInfo": {
                "totalResults": 1,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#channel",
                    "etag": "kajdkasa",
                    "id": "a random fr id",
                    "snippet": {
                        "title": "akyeiwiw",
                        "description": "",
                        "publishedAt": "2018-03-07T12:17:06Zt",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/ytc/gha",
                                "width": 88,
                                "height": 88
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/ytc/ayu",
                                "width": 240,
                                "height": 240
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/ytc/ryt",
                                "width": 800,
                                "height": 800
                            }
                        },
                        "localized": {
                            "title": "Yoogtt",
                            "description": ""
                        }
                    },
                    "contentDetails": {
                        "relatedPlaylists": {
                            "likes": "",
                            "uploads": "akjjal"
                        }
                    }
                }
            ]
        }
        expected_old_response = ChannelDetails(**first_mock_response["items"][0]).dict(exclude_unset=True)
        expected_updated_response = ChannelDetails(**second_mock_response["items"][0]).dict(exclude_unset=True)
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_updated_headers = {"Accept": "application/json", "Authorization": f"Bearer {other_access_token}"}
        expected_updated_headers = {"Accept": "application/json", "Authorization": f"Bearer {other_access_token}"}
        expected_url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={channel_id}&key=TEST_GOOGLE_API_KEY"
        expected_updated_url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={other_channel_id}&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=first_mock_response, status_code=200)
        self.client.get(f"/youtube/channels/{channel_id}", headers={"X-YouHedge-Token": access_token})

        # change the mock response
        mock_get.return_value = MockResponse(data=second_mock_response, status_code=200)

        # change headers and channel id and thus skip the cache
        new_headers_response = self.client.get(f"/youtube/channels/{other_channel_id}",
                                               headers={"X-YouHedge-Token": other_access_token})

        # use old headers and thus hit the cache
        old_headers_response = self.client.get(f"/youtube/channels/{channel_id}",
                                               headers={"X-YouHedge-Token": access_token})

        # wait for TTL to elapse and try the query again
        time.sleep(3)
        old_headers_after_sleep_response = self.client.get(f"/youtube/channels/{channel_id}",
                                                           headers={"X-YouHedge-Token": access_token})
        calls = [
            call(expected_url, headers=expected_headers),
            call(expected_updated_url, headers=expected_updated_headers),
            call(expected_url, headers=expected_headers),
        ]
        mock_get.assert_has_calls(calls=calls)
        self.assertEqual(200, old_headers_response.status_code)
        self.assertEqual(200, new_headers_response.status_code)
        self.assertEqual(200, old_headers_after_sleep_response.status_code)
        self.assertEqual(expected_updated_response, new_headers_response.json)
        self.assertEqual(expected_old_response, old_headers_response.json)
        self.assertEqual(expected_updated_response, old_headers_after_sleep_response.json)

    @patch("requests.get")
    def test_get_playlist_videos(self, mock_get: MagicMock):
        """Should return the PlaylistItemListResponse response after querying the YouTube data v3 endpoint"""
        access_token = "some dummy stuff-1"
        playlist_id = "a random playlist id"
        mock_response = {
            "kind": "youtube#playlistItemListResponse",
            "etag": "kshdyeiwuew",
            "nextPageToken": "aajhdaui",
            "items": [
                {
                    "kind": "youtube#playlistItem",
                    "etag": "aiuewewhjew",
                    "id": "OIUYUOhhldauiuwew",
                    "snippet": {
                        "publishedAt": "2022-07-27T18:04:50Z",
                        "channelId": "IUUAHsdaa",
                        "title": "eywuyewew",
                        "description": "Woohoo",
                        "thumbnails": {
                            "default": {
                                "url": "https://i.ytimg.com/vi/jkds/default.jpg",
                                "width": 120,
                                "height": 90
                            },
                            "medium": {
                                "url": "https://i.ytimg.com/vi/skfjs/mqdefault.jpg",
                                "width": 320,
                                "height": 180
                            },
                            "high": {
                                "url": "https://i.ytimg.com/vi/sfkjsfs/hqdefault.jpg",
                                "width": 480,
                                "height": 360
                            }
                        },
                        "channelTitle": "yupapisad",
                        "playlistId": "adkjada",
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "akjdajsu"
                        },
                        "videoOwnerChannelTitle": "yudaoad",
                        "videoOwnerChannelId": "adajhsdad"
                    }
                },
                {
                    "kind": "youtube#playlistItem",
                    "etag": "akdjlauiwew",
                    "id": "adjkalusdaiuda",
                    "snippet": {
                        "publishedAt": "2022-07-24T11:49:06Z",
                        "channelId": "sakjdkaluis",
                        "title": "adyuaywejhwhe",
                        "description": "hdauiuweiwelw",
                        "thumbnails": {
                            "default": {
                                "url": "https://i.ytimg.com/vi/jhsd/default.jpg",
                                "width": 120,
                                "height": 90
                            },
                            "medium": {
                                "url": "https://i.ytimg.com/vi/jksjdhj/mqdefault.jpg",
                                "width": 320,
                                "height": 180
                            },
                            "high": {
                                "url": "https://i.ytimg.com/vi/jsdhs/hqdefault.jpg",
                                "width": 480,
                                "height": 360
                            }
                        },
                        "channelTitle": "yuyewew",
                        "playlistId": "skdjss",
                        "position": 1,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "kjsjdjkshda"
                        },
                        "videoOwnerChannelTitle": "iywuewe",
                        "videoOwnerChannelId": "ajhdakhjsad"
                    }
                },
            ]
        }
        expected_response = PlaylistItemListResponse(**mock_response).dict(exclude_unset=True)
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=mock_response, status_code=200)

        response = self.client.get(f"/youtube/playlist-items/{playlist_id}", headers={"X-YouHedge-Token": access_token})
        mock_get.assert_called_with(expected_url, headers=expected_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response, response.json)

    @patch("requests.get")
    def test_cached_get_playlist_videos(self, mock_get: MagicMock):
        """Should return the cached PlaylistItemListResponse response for the given request if TTL is not yet exceeded"""
        access_token = "some dummy stuff-2"
        other_access_token = "wooohooo"
        playlist_id = "a random playlist id"
        other_playlist_id = "a random playls id"
        first_mock_response = {
            "kind": "youtube#playlistItemListResponse",
            "etag": "kshdyeiwuew",
            "nextPageToken": "aajhdaui",
            "items": [
                {
                    "kind": "youtube#playlistItem",
                    "etag": "aiuewewhjew",
                    "id": "OIUYUOhhldauiuwew",
                    "snippet": {
                        "publishedAt": "2022-07-27T18:04:50Z",
                        "channelId": "IUUAHsdaa",
                        "title": "eywuyewew",
                        "description": "Woohoo",
                        "thumbnails": {
                            "default": {
                                "url": "https://i.ytimg.com/vi/jkds/default.jpg",
                                "width": 120,
                                "height": 90
                            },
                            "medium": {
                                "url": "https://i.ytimg.com/vi/skfjs/mqdefault.jpg",
                                "width": 320,
                                "height": 180
                            },
                            "high": {
                                "url": "https://i.ytimg.com/vi/sfkjsfs/hqdefault.jpg",
                                "width": 480,
                                "height": 360
                            }
                        },
                        "channelTitle": "yupapisad",
                        "playlistId": "adkjada",
                        "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "akjdajsu"
                        },
                        "videoOwnerChannelTitle": "yudaoad",
                        "videoOwnerChannelId": "adajhsdad"
                    }
                }
            ]
        }
        second_mock_response = {
            "kind": "youtube#playlistItemListResponse",
            "etag": "kshdyeiwuew",
            "nextPageToken": "jahjye",
            "items": [
                {
                    "kind": "youtube#playlistItem",
                    "etag": "kjaj;uyr",
                    "id": "adjkalusdaiuda",
                    "snippet": {
                        "publishedAt": "2022-07-24T11:49:06Z",
                        "channelId": "sakjdkaluis",
                        "title": "adyuaywejhwhe",
                        "description": "kaue6w",
                        "thumbnails": {
                            "default": {
                                "url": "https://i.ytimg.com/vi/jhsd/default.jpg",
                                "width": 120,
                                "height": 90
                            },
                            "medium": {
                                "url": "https://i.ytimg.com/vi/jksjdhj/mqdefault.jpg",
                                "width": 320,
                                "height": 180
                            },
                            "high": {
                                "url": "https://i.ytimg.com/vi/jsdhs/hqdefault.jpg",
                                "width": 480,
                                "height": 360
                            }
                        },
                        "channelTitle": "yuyewew",
                        "playlistId": "skdjss",
                        "position": 1,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": "kjsjdjkshda"
                        },
                        "videoOwnerChannelTitle": "iywuewe",
                        "videoOwnerChannelId": "ajhdakhjsad"
                    }
                },
            ]
        }
        expected_old_response = PlaylistItemListResponse(**first_mock_response).dict(exclude_unset=True)
        expected_updated_response = PlaylistItemListResponse(**second_mock_response).dict(exclude_unset=True)
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_updated_headers = {"Accept": "application/json", "Authorization": f"Bearer {other_access_token}"}
        expected_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key=TEST_GOOGLE_API_KEY"
        expected_updated_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={other_playlist_id}&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=first_mock_response, status_code=200)
        self.client.get(f"/youtube/playlist-items/{playlist_id}", headers={"X-YouHedge-Token": access_token})

        # change the mock response
        mock_get.return_value = MockResponse(data=second_mock_response, status_code=200)

        # change headers and playlist id and thus skip the cache
        new_headers_response = self.client.get(f"/youtube/playlist-items/{other_playlist_id}",
                                               headers={"X-YouHedge-Token": other_access_token})

        # use old headers and thus hit the cache
        old_headers_response = self.client.get(f"/youtube/playlist-items/{playlist_id}",
                                               headers={"X-YouHedge-Token": access_token})

        # wait for TTL to elapse and try the query again
        time.sleep(3)
        old_headers_after_sleep_response = self.client.get(f"/youtube/playlist-items/{playlist_id}",
                                                           headers={"X-YouHedge-Token": access_token})
        calls = [
            call(expected_url, headers=expected_headers),
            call(expected_updated_url, headers=expected_updated_headers),
            call(expected_url, headers=expected_headers),
        ]
        mock_get.assert_has_calls(calls=calls)
        self.assertEqual(200, old_headers_response.status_code)
        self.assertEqual(200, new_headers_response.status_code)
        self.assertEqual(200, old_headers_after_sleep_response.status_code)
        self.assertEqual(expected_updated_response, new_headers_response.json)
        self.assertEqual(expected_old_response, old_headers_response.json)
        self.assertEqual(expected_updated_response, old_headers_after_sleep_response.json)


if __name__ == '__main__':
    main()
