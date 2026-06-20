import allure

from api.clients.user_api_client import UserApiClient
from tests.user.helpers import login_user, register_user


@allure.epic("User management")
@allure.feature("User editing")
class TestUserEdit:

    @allure.story("Positive edit scenario")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Edit just created user with valid data")
    @allure.tag("smoke", "regression", "positive")
    def test_edit_just_created_user(self, api: UserApiClient):
        register_data, user_id = register_user(api)
        session = login_user(api, register_data["email"], register_data["password"])

        new_name = "Changed Name"
        api.edit_user(user_id, {"firstName": new_name}, session.token, session.auth_sid)
        api.response_status_code_should_be(200)

        api.get_user(user_id, session.token, session.auth_sid)
        api.response_json_value_by_name_should_be(
            "firstName", new_name, "First name was not changed"
        )

    @allure.story("Security tests")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Unauthorized user edit attempt")
    @allure.tag("security", "regression", "negative")
    def test_edit_user_unauthorized(self, api: UserApiClient):
        register_data, user_id = register_user(api)
        session = login_user(api, register_data["email"], register_data["password"])

        api.edit_user(user_id, {"firstName": "Unauthorized Change"})
        api.response_status_code_should_be(400)

        api.get_user(user_id, session.token, session.auth_sid)
        api.response_json_value_by_name_should_be(
            "firstName",
            register_data["firstName"],
            "First name was changed despite unauthorized access",
        )

    @allure.story("Security tests")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Edit user as different user")
    @allure.tag("security", "regression", "negative")
    def test_edit_user_as_different_user(self, api: UserApiClient):
        register_data1, user_id_to_edit = register_user(api)
        session1 = login_user(api, register_data1["email"], register_data1["password"])

        register_data2, _ = register_user(api)
        session2 = login_user(api, register_data2["email"], register_data2["password"])

        api.edit_user(
            user_id_to_edit,
            {"firstName": "Changed By Other User"},
            session2.token,
            session2.auth_sid,
        )
        api.response_status_code_should_be_one_of((200, 400, 403))

        api.get_user(user_id_to_edit, session1.token, session1.auth_sid)
        api.response_json_value_by_name_should_be(
            "firstName",
            register_data1["firstName"],
            "First name was changed by another user",
        )

    @allure.story("Validation tests")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Edit with invalid email format")
    @allure.tag("validation", "regression", "negative")
    def test_edit_email_invalid_format(self, api: UserApiClient):
        register_data, user_id = register_user(api)
        session = login_user(api, register_data["email"], register_data["password"])
        email = register_data["email"]

        api.edit_user(
            user_id,
            {"email": "invalid.email.com"},
            session.token,
            session.auth_sid,
        )
        api.response_status_code_should_be(400)

        api.get_user(user_id, session.token, session.auth_sid)
        api.response_json_value_by_name_should_be(
            "email", email, "Email was changed to invalid format"
        )

    @allure.story("Validation tests")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Edit with too short first name")
    @allure.tag("validation", "regression", "negative")
    def test_edit_firstname_too_short(self, api: UserApiClient):
        register_data, user_id = register_user(api)
        session = login_user(api, register_data["email"], register_data["password"])

        api.edit_user(
            user_id,
            {"firstName": "A"},
            session.token,
            session.auth_sid,
        )
        api.response_status_code_should_be(400)

        api.get_user(user_id, session.token, session.auth_sid)
        api.response_json_value_by_name_should_be(
            "firstName",
            register_data["firstName"],
            "First name was changed to too short value",
        )
