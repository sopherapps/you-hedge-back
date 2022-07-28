"""Module containing tests for the youtube service"""

from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from services import create_app
from utils.testing import MockResponse

_app = create_app(config_filename="test.config.json")


class TestYoutube(TestCase):
    """Tests for the YouTube service"""

    def setUp(self) -> None:
        """Initialize a few common variables"""
        self.client = _app.test_client()

    @patch("requests.get")
    def test_get_subscriptions(self, mock_get: MagicMock):
        """Should return the SubscriptionListResponse response after querying the YouTube data v3 endpoint"""
        access_token = "some dummy stuff"
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
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_url = "https://youtube.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=mock_response, status_code=200)

        response = self.client.get("/youtube/subscriptions", headers={"X-YouHedge-Token": access_token})
        mock_get.assert_called_with(expected_url, headers=expected_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(mock_response, response.json)

    @patch("requests.get")
    def test_get_channel_details(self, mock_get: MagicMock):
        """Should return the ChannelDetailsResponse response after querying the YouTube data v3 endpoint"""
        access_token = "some dummy stuff"
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

        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={channel_id}&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=mock_response, status_code=200)

        response = self.client.get(f"/youtube/channels/{channel_id}", headers={"X-YouHedge-Token": access_token})
        mock_get.assert_called_with(expected_url, headers=expected_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(mock_response["items"][0], response.json)

    @patch("requests.get")
    def test_get_playlist_videos(self, mock_get: MagicMock):
        """Should return the PlaylistItemListResponse response after querying the YouTube data v3 endpoint"""
        access_token = "some dummy stuff"
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
        expected_headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
        expected_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key=TEST_GOOGLE_API_KEY"

        mock_get.return_value = MockResponse(data=mock_response, status_code=200)

        response = self.client.get(f"/youtube/playlist-items/{playlist_id}", headers={"X-YouHedge-Token": access_token})
        mock_get.assert_called_with(expected_url, headers=expected_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(mock_response, response.json)


if __name__ == '__main__':
    main()
