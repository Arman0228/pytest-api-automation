import datetime
import os

from requests import Response


class RequestLogger:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

    @classmethod
    def _log_file(cls) -> str:
        return os.path.join(
            cls.LOG_DIR,
            f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        )

    @classmethod
    def _write(cls, data: str) -> None:
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        with open(cls._log_file(), "a", encoding="utf-8") as log_file:
            log_file.write(data)

    @classmethod
    def add_request(
        cls,
        url: str,
        data: dict,
        headers: dict,
        cookies: dict,
        method: str,
    ) -> None:
        testname = os.environ.get("PYTEST_CURRENT_TEST", "")
        cls._write(
            f"\n-----\nTest: {testname}\nTime: {datetime.datetime.now()}\n"
            f"Request: {method} {url}\nData: {data}\nHeaders: {headers}\n"
            f"Cookies: {cookies}\n\n"
        )

    @classmethod
    def add_response(cls, response: Response) -> None:
        cls._write(
            f"Response code: {response.status_code}\n"
            f"Response text: {response.text}\n"
            f"Headers: {dict(response.headers)}\n"
            f"Cookies: {dict(response.cookies)}\n\n-----\n"
        )
