import allure
import pytest

from api.clients.user_api_client import UserApiClient
from tests.user.helpers import login_user, register_user
from tests.user.session import AuthSession


@allure.epic("Delete user cases")
@allure.feature("User deletion")
class TestPositiveUserDelete:

    @allure.label("section2", "Positive")
    @allure.story("Successful user deletion")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "regression", "positive")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_positive_delete_just_created_user(self, api: UserApiClient):
        register_data, user_id = register_user(api)
        session = login_user(api, register_data["email"], register_data["password"])

        api.delete_user(user_id, session.token, session.auth_sid)
        api.response_status_code_should_be(200)

        api.get_user(user_id)
        api.response_status_code_should_be(404)
        api.response_text_should_be("User not found")


@allure.epic("Delete user cases")
@allure.feature("User deletion")
class TestNegativeUserDelete:

    @allure.label("section2", "Negative")
    @allure.story("Protected user deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "regression", "negative")
    @pytest.mark.negative
    @pytest.mark.security
    def test_negative_delete_protected_user(
        self, api: UserApiClient, auth_session: AuthSession
    ):
        api.delete_user(2, auth_session.token, auth_session.auth_sid)
        api.response_status_code_should_be(400)
        api.response_json_value_by_name_should_be(
            "error",
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            "Unexpected response content",
        )

    @allure.label("section2", "Negative")
    @allure.story("Unauthorized user deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "regression", "negative")
    @pytest.mark.negative
    @pytest.mark.security
    def test_negative_delete_user_by_another_user(self, api: UserApiClient):
        register_data1, user_id_to_delete = register_user(api)
        register_data2, _ = register_user(api)
        session2 = login_user(api, register_data2["email"], register_data2["password"])

        api.delete_user(user_id_to_delete, session2.token, session2.auth_sid)

        session1 = login_user(api, register_data1["email"], register_data1["password"])
        api.get_user(user_id_to_delete, session1.token, session1.auth_sid)
        api.response_json_should_have_key("username")
