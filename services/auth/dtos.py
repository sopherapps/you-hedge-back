"""Data Transfer objects for auth"""
from utils.base_dto import BaseDto


class LoginDetails(BaseDto):
    device_code: str
    user_code: str
    verification_url: str
    expires_in: int
    interval: int


class LoginStatusResponse(BaseDto):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str


class RefreshTokenRequest(BaseDto):
    refresh_token: str


class RefreshTokenResponse(BaseDto):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
