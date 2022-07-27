"""Module containing functionality for getting Youtube data"""
from flask import Blueprint, request

bp = Blueprint("youtube", __name__, url_prefix="/youtube")


@bp.get("/subscriptions")
def get_subscriptions():
    """Returns the subscriptions belonging to the logged in user"""
    pass


@bp.get("/channels/<string:channel_id>")
def get_channel_details(channel_id: str):
    """Responds with the details for the given channel"""
    pass


@bp.get("/playlists/<string:playlist_id>/videos")
def get_playlist_videos(playlist_id: str):
    """
    Gets the list of videos for the given playlist in a paginated fashion
    A channel has at least one playlist
    """
    next_page_token = request.args.get("nextPageToken", None)

    pass
