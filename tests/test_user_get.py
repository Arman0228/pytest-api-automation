import allure

from api.clients.user_api_client import UserApiClient
from tests.user.session import AuthSession


@allure.epic("User data access")
@allure.feature("User details retrieval")
class TestUserGet:

    @allure.story("Unauthorized access")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    @allure.description("Unauthorized user can only see username")
    def test_get_user_details_not_auth(self, api: UserApiClient):
        api.get_user(2)
        api.response_json_should_have_key("username")
        api.response_json_should_not_have_key("email")
        api.response_json_should_not_have_key("firstName")
        api.response_json_should_not_have_key("lastName")

    @allure.story("Authorized access")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive")
    @allure.description("Authorized user can see all own details")
    def test_get_user_details_auth_as_same_user(
        self, api: UserApiClient, auth_session: AuthSession
    ):
        api.get_user(auth_session.user_id, auth_session.token, auth_session.auth_sid)
        api.response_json_should_have_keys(
            ["username", "email", "firstName", "lastName"]
        )

    @allure.story("Cross-user access")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("security", "negative")
    @allure.description("User cannot see private details of another user")
    def test_get_user_details_auth_as_different_user(
        self, api: UserApiClient, auth_session: AuthSession
    ):
        different_user_id = 1
        if different_user_id == auth_session.user_id:
            different_user_id = auth_session.user_id + 1

        api.get_user(different_user_id, auth_session.token, auth_session.auth_sid)
        api.response_json_should_have_key("username")
        api.response_json_should_not_have_key("email")
        api.response_json_should_not_have_key("firstName")
        api.response_json_should_not_have_key("lastName")
