"""Module for utilities for tests"""
from typing import Dict, Any


class MockResponse:
    def __init__(self, data: Dict[str, Any], status_code: int):
        self._data = data
        self._status_code = status_code

    def ok(self) -> bool:
        return self._status_code < 400

    def json(self) -> Dict[str, Any]:
        return self._data
