"""Module containing client code for authenticating with Google account via the TV flow"""
import requests

from utils.exc import APIException
from .dtos import LoginDetails, LoginStatusResponse, RefreshTokenResponse, RefreshTokenRequest


def initialize_tv_login(client_id) -> LoginDetails:
    """
    Initializes the login with google via the TV device flow.
    It will return a url and a code for a user to login via a phone or desktop
    https://developers.google.com/identity/gsi/web/guides/devices
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = "https://oauth2.googleapis.com/device/code"
    data = {
        "client_id": client_id,
        "scope": "https://www.googleapis.com/auth/youtube.readonly"
    }
    response = requests.post(url, data=data, headers=headers)
    if not response.ok:
        raise APIException(message="unknown internal error", status_code=500)

    return LoginDetails.validate(response.json())



def check_tv_login_status(device_id: str, interval: int) -> LoginStatusResponse:
    """
    Checks whether the user has logged in at the given verification url.
    It will poll until it gets something a response other than "error" : "authorization_pending".
    If it gets "error" : "slow_down", it will double the interval and continue polling
    """
    raise NotImplementedError("todo")


def refresh_access_token(request: RefreshTokenRequest) -> RefreshTokenResponse:
    """
    Refreshes the access token associated with the refresh token provided and returns the new acces token
    details
    """
    raise NotImplementedError("todo")
