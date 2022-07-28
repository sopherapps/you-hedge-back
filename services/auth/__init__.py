"""Service for handling logins"""
from flask import Blueprint, request, current_app

from utils.view_utils import body_required
from . import client
from .dtos import RefreshTokenRequest

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/tv")
def tv_login():
    """
    Initializes logging in via TV, returning a verification link
    and a User code for user to login with
    """
    response = client.initialize_tv_login(
        client_id=current_app.config["GOOGLE_CLIENT_ID"])
    return response.jsonify(current_app)


@bp.get("/tv/<string:device_id>")
def check_tv_login_status(device_id: str):
    """
    Finalizes the logging in via TV after the user has visited
    the verification link on their mobile or desktop.
    It checks the Google endpoint at the given interval in seconds
    passed as a query parameter to see the status of the login request
    """
    interval: int = request.args.get("interval", 5, int)
    response = client.check_tv_login_status(
        device_id=device_id,
        interval=interval,
        client_id=current_app.config["GOOGLE_CLIENT_ID"],
        client_secret=current_app.config["GOOGLE_CLIENT_SECRET"],
        timeout=current_app.config["HTTP_REQUEST_TIMEOUT"],
    )
    return response.jsonify(current_app)


@bp.post("/refresh-token")
@body_required(RefreshTokenRequest)
def refresh_token(body: RefreshTokenRequest):
    """
    Refreshes the token associated with the passed refresh_token and responds with a new token
    """
    response = client.refresh_access_token(body)
    return response.jsonify(current_app)
