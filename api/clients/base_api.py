import json
from pathlib import Path
from typing import Any

import allure
import requests
from jsonschema import validate
from requests import Response

from config.settings import settings
from lib.logger import Logger


class BaseApi:
    def __init__(self) -> None:
        self.response: Response | None = None

    def _full_url(self, path: str) -> str:
        return f"{settings.get_base_url()}{path}"

    def _send(
        self,
        method: str,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
    ) -> "BaseApi":
        data = data or {}
        headers = headers or {}
        cookies = cookies or {}
        url = self._full_url(path)

        with allure.step(f"{method} {path}"):
            Logger.add_request(url, data, headers, cookies, method)
            if method == "GET":
                self.response = requests.get(url, headers=headers, cookies=cookies, params=data)
            elif method == "POST":
                self.response = requests.post(url, headers=headers, cookies=cookies, data=data)
            elif method == "PUT":
                self.response = requests.put(url, headers=headers, cookies=cookies, data=data)
            elif method == "DELETE":
                self.response = requests.delete(url, headers=headers, cookies=cookies, data=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            Logger.add_response(self.response)

        return self

    def get(
        self,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
    ) -> "BaseApi":
        return self._send("GET", path, data, headers, cookies)

    def post(
        self,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
    ) -> "BaseApi":
        return self._send("POST", path, data, headers, cookies)

    def put(
        self,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
    ) -> "BaseApi":
        return self._send("PUT", path, data, headers, cookies)

    def delete(
        self,
        path: str,
        data: dict | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
    ) -> "BaseApi":
        return self._send("DELETE", path, data, headers, cookies)

    def _json(self) -> dict:
        assert self.response is not None, "No response stored"
        try:
            return self.response.json()
        except json.JSONDecodeError as exc:
            raise AssertionError(
                f"Response is not JSON. Text: {self.response.text}"
            ) from exc

    def get_cookie(self, name: str) -> str:
        assert self.response is not None
        assert name in self.response.cookies, f"Cookie '{name}' not found"
        return self.response.cookies[name]

    def get_header(self, name: str) -> str:
        assert self.response is not None
        assert name in self.response.headers, f"Header '{name}' not found"
        return self.response.headers[name]

    def get_json_value(self, name: str) -> Any:
        body = self._json()
        assert name in body, f"JSON key '{name}' not found"
        return body[name]

    def response_status_code_should_be(self, expected: int) -> "BaseApi":
        assert self.response is not None
        assert self.response.status_code == expected, (
            f"Expected status {expected}, got {self.response.status_code}"
        )
        return self

    def response_json_should_have_key(self, key: str) -> "BaseApi":
        body = self._json()
        assert key in body, f"JSON key '{key}' not found"
        return self

    def response_json_should_have_keys(self, keys: list[str]) -> "BaseApi":
        body = self._json()
        for key in keys:
            assert key in body, f"JSON key '{key}' not found"
        return self

    def response_json_should_not_have_key(self, key: str) -> "BaseApi":
        body = self._json()
        assert key not in body, f"JSON key '{key}' should be absent"
        return self

    def response_json_value_by_name_should_be(
        self, name: str, expected: Any, message: str = ""
    ) -> "BaseApi":
        body = self._json()
        assert name in body, f"JSON key '{name}' not found"
        assert body[name] == expected, message or f"{name} != {expected}"
        return self

    def response_status_code_should_be_one_of(self, expected: tuple[int, ...]) -> "BaseApi":
        assert self.response is not None
        assert self.response.status_code in expected, (
            f"Expected one of {expected}, got {self.response.status_code}"
        )
        return self

    def response_text_should_be(self, expected: str) -> "BaseApi":
        assert self.response is not None
        assert self.response.text == expected, (
            f"Expected text '{expected}', got '{self.response.text}'"
        )
        return self

    def response_text_should_contain(self, substring: str) -> "BaseApi":
        assert self.response is not None
        assert substring in self.response.text, (
            f"Expected substring '{substring}' in response: {self.response.text}"
        )
        return self

    def response_body_should_match_schema(self, schema_path: Path) -> "BaseApi":
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validate(instance=self._json(), schema=schema)
        return self
