"""Service for handling logins"""
from flask import Blueprint, request

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/tv")
def tv_login():
    """
    Initializes logging in via TV, returning a verification link
    and a User code for user to login with
    """
    pass


@bp.get("/tv/<string:device_id>")
def check_tv_login_status(device_id: str):
    """
    Finalizes the logging in via TV after the user has visited
    the verification link on their mobile or desktop.
    It checks the Google endpoint at the given interval in seconds
    passed as a query parameter to see the status of the login request
    """
    interval: int = request.args.get("interval", 5, int)
    pass


@bp.post("/refresh-token")
def refresh_token():
    """
    Refreshes the token associated with the passed refresh_token and responds with a new token
    Body: RefreshTokenRequest
    Response: RefreshTokenResponse
    :return:
    """
    pass

