"""Module containing exceptions"""
from typing import Any, Dict

import orjson


class APIException(Exception):
    def __init__(self, message: str, status_code: int, payload: Any = None):
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def bjson(self) -> bytes:
        """Converts error to JSON in bytes"""
        return orjson.dumps(dict(error=self.message))

    def to_dict(self) -> Dict[str, Any]:
        """Returns the exception as a dictionary"""
        return dict(message=self.message, status_code=self.status_code, payload=self.payload)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.to_dict()}"
