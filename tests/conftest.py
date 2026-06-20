import pytest

from api.clients.user_api_client import UserApiClient
from tests.user.data import DEFAULT_TEST_USER
from tests.user.session import AuthSession


@pytest.fixture
def api() -> UserApiClient:
    return UserApiClient()


@pytest.fixture
def default_user_creds() -> dict:
    return DEFAULT_TEST_USER.copy()


@pytest.fixture
def auth_session(api: UserApiClient, default_user_creds: dict) -> AuthSession:
    api.login(default_user_creds["email"], default_user_creds["password"])
    return AuthSession(
        auth_sid=api.get_cookie("auth_sid"),
        token=api.get_header("x-csrf-token"),
        user_id=api.get_json_value("user_id"),
    )
