"""Tests for the auth service"""
from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call

from services import create_app
from utils.testing import MockResponse

_app = create_app(config_filename="test.config.json", should_log_err_to_file=False)


class TestAuth(TestCase):
    """Tests for the auth service"""

    def setUp(self) -> None:
        """Create a few common variables"""
        self.client = _app.test_client()

    @patch("requests.post")
    def test_tv_login(self, mock_post: MagicMock):
        """Should return the LoginDetails after making a call to the Google authentication endpoint"""
        mock_login_details = {
            "device_code": "4/4-GMMhmHCXhWEzkobqIHGG_EnNYYsAkukHspeYUk9E8",
            "user_code": "GQVQ-JKEC",
            "verification_url": "https://www.google.com/device",
            "expires_in": 1800,
            "interval": 5
        }
        expected_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        expected_url = "https://oauth2.googleapis.com/device/code"
        expected_data = {
            "client_id": "TEST_GOOGLE_CLIENT_ID",
            "scope": "https://www.googleapis.com/auth/youtube.readonly"
        }
        mock_post.return_value = MockResponse(data=mock_login_details, status_code=200)

        response = self.client.post("/auth/tv", json={})
        mock_post.assert_called_with(expected_url, headers=expected_headers, data=expected_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(mock_login_details, response.json)

    @patch("requests.post")
    def test_check_tv_login_status(self, mock_post: MagicMock):
        """Should return the LoginStatusResponse after polling Google token endpoint"""
        device_code = "random stuff"
        interval = 2
        mock_login_status = {
            "access_token": "ya29.AHES6ZSuY8f6WFLswSv0HZLP2J4cCvFSj-8GiZM0Pr6cgXU",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "1/551G1yXUqgkDGnkfFk6ZbjMMMDIMxo3JFc8lY8CAR-Q",
        }
        expected_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        expected_url = "https://oauth2.googleapis.com/token"
        expected_data = {
            "client_id": "TEST_GOOGLE_CLIENT_ID",
            "client_secret": "TEST_GOOGLE_CLIENT_SECRET",
            "code": device_code,
            "grant_type": "http://oauth.net/grant_type/device/1.0"
        }
        expected_responses = [
            {"error": "authorization_pending"},
            {"error": "authorization_pending"},
            {"error": "authorization_pending"},
            {**mock_login_status, "id_token": "eyJhbGciOiJSUzI..."}
        ]
        expected_responses_iter = (resp for resp in expected_responses)

        def mock_login_status_check(*args, **kwargs):
            status_code = 404
            data = next(expected_responses_iter)
            if data.get("error", None) is None:
                status_code = 200

            return MockResponse(data=data, status_code=status_code)

        mock_post.side_effect = mock_login_status_check

        response = self.client.get(f"/auth/tv/{device_code}", query_string={"interval": interval})
        calls = [call(expected_url, headers=expected_headers, data=expected_data) for _ in expected_responses]

        mock_post.assert_has_calls(calls=calls)
        self.assertEqual(200, response.status_code)
        self.assertEqual(mock_login_status, response.json)

    @patch("requests.post")
    def test_refresh_token(self, mock_post: MagicMock):
        """Should return the RefreshTokenResponse after making a call to the Google token refresh endpoint"""
        refresh_token = "some random token"
        mock_refresh_token_response = {
            "access_token": "1/fFAGRNJru1FTz70BzhT3Zg",
            "expires_in": 3920,
            "scope": "https://www.googleapis.com/auth/drive.metadata.readonly",
            "token_type": "Bearer"
        }
        expected_headers = {"Content-Type": "application/x-www-form-urlencoded"}
        expected_url = "https://oauth2.googleapis.com/token"
        expected_data = {
            "client_id": "TEST_GOOGLE_CLIENT_ID",
            "client_secret": "TEST_GOOGLE_CLIENT_SECRET",
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        mock_post.return_value = MockResponse(data=mock_refresh_token_response, status_code=200)

        response = self.client.post("/auth/refresh-token", json={"refresh_token": refresh_token})
        mock_post.assert_called_with(expected_url, headers=expected_headers, data=expected_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(mock_refresh_token_response, response.json)


if __name__ == '__main__':
    main()
