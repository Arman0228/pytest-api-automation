from api.clients.user_api_client import UserApiClient
from tests.user.data import build_registration_body
from tests.user.session import AuthSession


def register_user(api: UserApiClient, email: str | None = None) -> tuple[dict, int]:
    data = build_registration_body(email)
    api.register(data).response_status_code_should_be(200).response_json_should_have_key("id")
    return data, api.get_json_value("id")


def login_user(api: UserApiClient, email: str, password: str) -> AuthSession:
    api.login(email, password).response_status_code_should_be(200)
    return AuthSession(
        auth_sid=api.get_cookie("auth_sid"),
        token=api.get_header("x-csrf-token"),
        user_id=api.get_json_value("user_id"),
    )
