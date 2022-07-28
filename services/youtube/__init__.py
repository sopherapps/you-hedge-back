"""Module containing functionality for getting Youtube data"""
from flask import Blueprint, request, current_app

from utils.view_utils import auth_token_required
from . import client

bp = Blueprint("youtube", __name__, url_prefix="/youtube")


@bp.get("/subscriptions")
@auth_token_required
def get_subscriptions(access_token: str):
    """Returns the subscriptions belonging to the logged-in user"""
    next_page_token = request.args.get("nextPageToken", None)
    prev_page_token = request.args.get("prevPageToken", None)
    response = client.get_subscriptions(
        access_token=access_token,
        api_key=current_app.config["GOOGLE_API_KEY"],
        next_page_token=next_page_token,
        prev_page_token=prev_page_token,
    )
    return response.jsonify(current_app)


@bp.get("/channels/<string:channel_id>")
@auth_token_required
def get_channel_details(channel_id: str, access_token: str):
    """Responds with the details for the given channel"""
    next_page_token = request.args.get("nextPageToken", None)
    prev_page_token = request.args.get("prevPageToken", None)
    response = client.get_channel_details(
        channel_id=channel_id,
        api_key=current_app.config["GOOGLE_API_KEY"],
        access_token=access_token,
        next_page_token=next_page_token,
        prev_page_token=prev_page_token)
    return response.jsonify(current_app)


@bp.get("/playlist-items/<string:playlist_id>")
@auth_token_required
def get_playlist_videos(playlist_id: str, access_token: str):
    """
    Gets the list of videos for the given playlist in a paginated fashion
    A channel has at least one playlist
    """
    next_page_token = request.args.get("nextPageToken", None)
    prev_page_token = request.args.get("prevPageToken", None)
    response = client.get_playlist_items(
        playlist_id=playlist_id,
        api_key=current_app.config["GOOGLE_API_KEY"],
        access_token=access_token,
        next_page_token=next_page_token,
        prev_page_token=prev_page_token)
    return response.jsonify(current_app)
