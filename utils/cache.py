"""Module containing utilities to cache requests basing on headers, url and data"""

import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional

from flask import request, Request, has_request_context, Response


class ChecksumCalcStream(object):
    """
    Computes a SHA1 hash as the request stream is being consumed.
    It should thus be initialized before the request stream is accessed e.g. via request.headers
    This hash will help us decide whether the given request exists in the cache or not
    """

    def __init__(self, stream):
        self._stream = stream
        self._hash = hashlib.sha1()

    def read(self, byte_data):
        rv = self._stream.read(byte_data)
        self._hash.update(rv)
        return rv

    def readline(self, size_hint):
        rv = self._stream.readline(size_hint)
        self._hash.update(rv)
        return rv


def get_checksum(req: Request):
    """
    Initializes the checksum generator for a given request if it has not yet been initialized
    and returns it
    """
    env = request.environ
    stream = ChecksumCalcStream(env['wsgi.input'])
    env['wsgi.input'] = stream
    return stream._hash


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
            checksum = get_checksum(request)
            # read the stream so that the checksum is completed
            _ = request.data
            key = checksum.hexdigest()
            value = self[key]

            if value is None:
                value: Response = view(*args, **kwargs)
                if value.status_code < 400:
                    # save only successful requests
                    self[key] = value

            return value

        return view(*args, **kwargs)

    def clear(self):
        """Clears all the data in the cache"""
        self._data.clear()
