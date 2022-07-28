"""Module containing exceptions"""
import orjson


class APIException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

    def bjson(self) -> bytes:
        """Converts error to JSON in bytes"""
        return orjson.dumps(dict(error=self.message))
