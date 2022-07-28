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


class PlayListDetails(BaseDto):
    uploads: Optional[str] = None


class ChannelSnippet(BaseDto):
    title: str
    description: str
    thumbnails: ThumbnailDetails


class ChannelContentDetails(BaseDto):
    relatedPlaylists: PlayListDetails


class ChannelDetails(BaseDto):
    id: str
    snippet: ChannelSnippet
    contentDetails: ChannelContentDetails


class PageInfo(BaseDto):
    totalResults: int
    resultsPerPage: int


class VideoResourceId(BaseDto):
    videoId: str


class PlaylistItemSnippet(BaseDto):
    title: str
    description: str
    thumbnails: ThumbnailDetails
    position: int
    resourceId: VideoResourceId


class PlaylistItem(BaseDto):
    id: str
    snippet: PlaylistItemSnippet


class SubscriptionResourceId(BaseDto):
    channelId: str


class SubscriptionSnippet(BaseDto):
    title: str
    description: str
    resourceId: SubscriptionResourceId
    thumbnails: ThumbnailDetails


class SubscriptionDetails(BaseDto):
    id: str
    snippet: SubscriptionSnippet


# Responses
class BaseResponse(BaseDto):
    """The base class for all HTTP responses from YouTube data v3"""
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
