"""Module containing utilities to cache requests basing on headers, url and data"""
from datetime import datetime, timedelta
from io import BytesIO
from typing import Dict, Any, Tuple, Optional

from flask import request, Request, has_request_context, Response


def get_req_id(req: Request) -> str:
    """
    returns a request id constructed from the url, method, query params, headers and body
    """
    body = read_request_body_without_consuming_it(req)
    return f"{req.url}{req.query_string}{req.method}{body}{req.headers}"


def read_request_body_without_consuming_it(req: Request) -> bytes:
    """
    Reads the body of a request without consuming it so that future calls to request.data
    don't get surprised at any empty string
    """
    length = int(req.environ.get('CONTENT_LENGTH') or 0)
    body = req.environ['wsgi.input'].read(length)
    req.environ['body_copy'] = body
    # replace the stream since it was exhausted by read()
    req.environ['wsgi.input'] = BytesIO(body)
    return req.environ['body_copy']


class Cache:
    """The cache is basically a dictionary in memory whose values have time-to-live (TTL)"""

    def __init__(self, ttl: int):
        self._data: Dict[str, Tuple[Any, datetime]] = {}
        self._ttl: timedelta = timedelta(seconds=ttl)

    def __getitem__(self, item: Any) -> Optional[Any]:
        """
        Returns the value corresponding to the given item or key.
        It is None if it is older that ttl or if it does not exist
        """
        value: Optional[Tuple[Any, datetime]] = self._data.get(item, None)
        if value is None:
            return None

        if (datetime.now() - value[1]) > self._ttl:
            del self._data[item]
            return None

        return value[0]

    def __setitem__(self, key, value):
        """Sets a given key value in the cache with its new start time"""
        self._data[key] = (value, datetime.now())

    def get_view(self, view, *args, **kwargs):
        """Gets the cached response of the view if it exists"""
        if has_request_context():
            request_id = get_req_id(request)
            value = self[request_id]

            if value is None:
                value: Response = view(*args, **kwargs)
                if value.status_code < 400:
                    # save only successful requests
                    self[request_id] = value

            return value

        return view(*args, **kwargs)

    def clear(self):
        """Clears all the data in the cache"""
        self._data.clear()
