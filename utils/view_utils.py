"""Module containing utility functions concerned with views app"""
import functools
from typing import Type

from flask import request, current_app
from pydantic import ValidationError

from utils.base_dto import BaseDto
from utils.exc import APIException


def auth_token_required(view):
    """Decorator to ensure the given view has the token passed as a Header X-YouHedge-Token"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        access_token = request.headers.get("X-YouHedge-Token", None)
        if access_token is None:
            raise APIException(message="Missing 'X-YouHedge-Token' header", status_code=401)

        return view(**kwargs, access_token=access_token)

    return wrapped_view


def body_required(request_model: Type[BaseDto]):
    """Decorator to ensure that the JSON body passed to the view is of the given Type"""
    def wrapped_view(view):
        @functools.wraps(view)
        def inner_view(**kwargs):
            try:
                body = request_model.validate(request.json)
                return view(**kwargs, body=body)
            except ValidationError:
                raise APIException(message="malformed body", status_code=400)

        return inner_view

    return wrapped_view


def cached(view):
    """Ensures that the wrapped view hits the cache first before it tries the full request"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        cache = current_app.config["CACHE"]
        return cache.get_view(view, **kwargs)

    return wrapped_view
