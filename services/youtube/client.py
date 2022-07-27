"""Module containing the client code for YouTube data v3 API"""
from typing import Optional, List

from .dtos import SubscriptionListResponse, ChannelDetailsResponse, PlaylistItemListResponse


def get_subscriptions(
        access_token: str,
        next_page_token: Optional[str] = None,
        prev_page_token: Optional[str] = None) -> SubscriptionListResponse:
    """Gets the list of subscriptions for the given user"""
    raise NotImplementedError("implement this")


def get_channel_details(
        channel_id: str,
        access_token: str,
        next_page_token: Optional[str] = None,
        prev_page_token: Optional[str] = None) -> ChannelDetailsResponse:
    """Gets the details of the channel of the given channel id"""
    raise NotImplementedError("implement this")


def get_playlist_items(
        playlist_id: str,
        access_token: str,
        next_page_token: Optional[str] = None,
        prev_page_token: Optional[str] = None) -> PlaylistItemListResponse:
    """Gets the items in the playlist of the given playlist id"""
    raise NotImplementedError("implement this")
