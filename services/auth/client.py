"""Module containing client code for authenticating with Google account via the TV flow"""
import time
from datetime import datetime, timedelta
from http import HTTPStatus

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


def check_tv_login_status(
        device_id: str,
        interval: int,
        client_id: str,
        client_secret: str,
        timeout: int,
) -> LoginStatusResponse:
    """
    Checks whether the user has logged in at the given verification url.
    It will poll until it gets something a response other than "error" : "authorization_pending".
    If it gets "error" : "slow_down", it will double the interval and continue polling
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "device_code": device_id,
        "grant_type": "http://oauth.net/grant_type/device/1.0"
    }
    timeout = timedelta(seconds=timeout)
    start_time = datetime.now()

    while datetime.now() - start_time < timeout:
        response = requests.post(url, data=data, headers=headers)
        if response.ok:
            return LoginStatusResponse.validate(response.json())
        else:
            try:
                error = response.json().get("error", None)
                if error == 'slow_down':
                    interval *= 2
                elif error == 'authorization_pending':
                    time.sleep(interval)
                else:
                    raise APIException(message="unknown internal error", status_code=500)

            except requests.exceptions.JSONDecodeError:
                raise APIException(message="unexpected internal error", status_code=500)

    raise APIException(message="timeout error", status_code=HTTPStatus.REQUEST_TIMEOUT)


def refresh_access_token(
        request: RefreshTokenRequest,
        client_id: str,
        client_secret: str) -> RefreshTokenResponse:
    """
    Refreshes the access token associated with the refresh token provided and returns the new acces token
    details
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": request.refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=data, headers=headers)
    if not response.ok:
        raise APIException(message="unknown internal error", status_code=500)

    return RefreshTokenResponse.validate(response.json())
