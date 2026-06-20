import allure
import pytest

from api.clients.user_api_client import UserApiClient
from tests.user.paths import SCHEMAS_DIR
from tests.user.session import AuthSession


@allure.epic("Authorization cases")
@allure.feature("User authentication")
class TestPositiveUserAuth:

    @allure.label("section2", "Positive")
    @allure.story("Successful authentication")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive", "authentication")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_positive_auth_user(self, api: UserApiClient, auth_session: AuthSession):
        api.auth(auth_session.token, auth_session.auth_sid)
        api.response_json_value_by_name_should_be(
            "user_id",
            auth_session.user_id,
            "User id from auth method is not equal to user id from check method",
        ).response_body_should_match_schema(SCHEMAS_DIR / "user_auth_200.json")


@allure.epic("Authorization cases")
@allure.feature("User authentication")
class TestNegativeUserAuth:
    exclude_params = [
        ("no_cookie", allure.severity_level.NORMAL),
        ("no_token", allure.severity_level.NORMAL),
    ]

    @allure.label("section2", "Negative")
    @allure.story("Negative authentication scenarios")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative", "authentication")
    @pytest.mark.negative
    @pytest.mark.security
    @pytest.mark.parametrize("condition,severity", exclude_params)
    def test_negative_auth_check(
        self, api: UserApiClient, auth_session: AuthSession, condition: str, severity
    ):
        if condition == "no_cookie":
            api.get(
                "/user/auth",
                headers={"x-csrf-token": auth_session.token},
            )
        else:
            api.get(
                "/user/auth",
                cookies={"auth_sid": auth_session.auth_sid},
            )

        api.response_json_value_by_name_should_be(
            "user_id",
            0,
            f"User is authorized with condition {condition}",
        )
