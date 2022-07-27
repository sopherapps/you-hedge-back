from datetime import datetime
from typing import List, Optional, Any

from utils.base_dto import BaseDto


class Thumbnail(BaseDto):
    url: str
    width: Optional[int] = None
    height: Optional[int] = None


class ThumbnailDetails(BaseDto):
    default: Optional[Thumbnail] = None
    medium: Optional[Thumbnail] = None
    high: Optional[Thumbnail] = None
    standard: Optional[Thumbnail] = None
    maxres: Optional[Thumbnail] = None


class LocalizedChannelDetails(BaseDto):
    title: str
    description: str


class PlayListDetails(BaseDto):
    likes: str
    uploads: str


class ChannelSnippet(BaseDto):
    title: str
    description: str
    publishedAt: datetime
    thumbnails: ThumbnailDetails
    localized: LocalizedChannelDetails


class ChannelContentDetails(BaseDto):
    relatedPlaylist: PlayListDetails


class ChannelDetails(BaseDto):
    kind: str
    etag: str
    id: str
    snippet: ChannelSnippet
    contentDetails: ChannelContentDetails


class PageInfo(BaseDto):
    totalResult: int
    resultsPerPage: int


class VideoResourceId(BaseDto):
    kind: str
    videoId: str


class PlaylistItemSnippet(BaseDto):
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: ThumbnailDetails
    channelTitle: str
    playlistId: str
    position: int
    resourceId: VideoResourceId


class PlaylistItem(BaseDto):
    kind: str
    etag: str
    id: str
    snippet: PlaylistItemSnippet
    videoOwnerChannelTitle: str
    videoOwnerChannelId: str


class SubscriptionResourceId(BaseDto):
    kind: str
    channelId: str


class SubscriptionSnippet(BaseDto):
    publishedAt: datetime
    title: str
    description: str
    resourceId: SubscriptionResourceId
    channelId: str
    thumbnails: ThumbnailDetails


class SubscriptionDetails(BaseDto):
    kind: str
    etag: str
    id: str
    snippet: SubscriptionSnippet


# Responses
class BaseResponse(BaseDto):
    """The base class for all HTTP responses from YouTube data v3"""
    kind: str
    etag: str
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    pageInfo: Optional[PageInfo] = None
    items: List[Any]


class ChannelDetailsResponse(BaseResponse):
    """
    The response returned from YouTube data API v3 when requesting for channel details
    https://developers.google.com/youtube/v3/docs/channels/list?apix_params=%7B%22part%22%3A%5B%22snippet%2CcontentDetails%22%5D%2C%22id%22%3A%5B%22UCpyvKj4fs50RhBMrQXynbtw%22%5D%7D&apix=true
    """
    items: List[ChannelDetails]


class PlaylistItemListResponse(BaseResponse):
    """
    The response from YouTube data API v3 when requesting for items in a given playlist
    https://developers.google.com/youtube/v3/docs/playlistItems/list?apix_params=%7B%22part%22%3A%5B%22snippet%22%5D%2C%22playlistId%22%3A%22UUpyvKj4fs50RhBMrQXynbtw%22%7D&apix=true
    """
    items: List[PlaylistItem]


class SubscriptionListResponse(BaseResponse):
    """
    The response from YouTube data API v3 when requesting for a user's subscription list
    https://developers.google.com/youtube/v3/docs/subscriptions/list?apix_params=%7B%22part%22%3A%5B%22snippet%22%5D%2C%22mine%22%3Atrue%7D&apix=true#usage
    """
    items: List[SubscriptionDetails]
