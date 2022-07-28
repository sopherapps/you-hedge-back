"""Module containing the client code for YouTube data v3 API"""
from typing import Optional

import requests

from utils.exc import APIException
from .dtos import SubscriptionListResponse, PlaylistItemListResponse, ChannelDetails, ChannelDetailsResponse


def get_subscriptions(
        api_key: str,
        access_token: str,
        page_token: Optional[str] = None) -> SubscriptionListResponse:
    """Gets the list of subscriptions for the given user"""
    headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://youtube.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true&key={api_key}"
    if page_token is not None:
        url = f"{url}&pageToken={page_token}"

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise APIException(message=f"unknown internal error", status_code=500, payload=response.json())

    return SubscriptionListResponse.validate(response.json())


def get_channel_details(
        channel_id: str,
        api_key: str,
        access_token: str,
        page_token: Optional[str] = None) -> ChannelDetails:
    """Gets the details of the channel of the given channel id"""
    headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={channel_id}&key={api_key}"
    if page_token is not None:
        url = f"{url}&pageToken={page_token}"

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise APIException(message="unknown internal error", status_code=500, payload=response.json())

    parsed_response = ChannelDetailsResponse.validate(response.json())
    return parsed_response.items[0]


def get_playlist_items(
        playlist_id: str,
        api_key: str,
        access_token: str,
        page_token: Optional[str] = None) -> PlaylistItemListResponse:
    """Gets the items in the playlist of the given playlist id"""
    headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
    url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={api_key}"
    if page_token is not None:
        url = f"{url}&pageToken={page_token}"

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise APIException(message="unknown internal error", status_code=500, payload=response.json())

    return PlaylistItemListResponse.validate(response.json())
