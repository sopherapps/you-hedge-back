"""Module containing utility functions concerned with views app"""
import functools
from typing import Callable, Type

from flask import request
from pydantic import ValidationError

from utils.base_dto import BaseDto


def auth_token_required(view):
    """Decorator to ensure the given view has the token passed as a Header X-YouHedge-Token"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        access_token = request.headers.get("X-YouHedge-Token", None)
        if access_token is None:
            return {"error": "Missing 'X-YouHedge-Token' header"}, 401

        return view(**kwargs, access_token=access_token)

    return wrapped_view


def body_required(request_model: Type[BaseDto]):
    """Decorator to ensure that the JSON body passed to the view is of the given Type"""
    def wrapped_view(view):
        @functools.wraps(view)
        def inner_view(**kwargs):
            body = request.json()
            try:
                body = request_model.validate(body)
            except ValidationError:
                return {"error": "malformed body"}, 400

            return view(**kwargs, body=body)

        return inner_view

    return wrapped_view
