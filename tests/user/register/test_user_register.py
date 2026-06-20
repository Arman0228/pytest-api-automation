import pytest
import allure

from api.clients.user_api_client import UserApiClient
from tests.user.data import EXISTING_USER_EMAIL, build_registration_body


@allure.epic("User registration")
@allure.feature("User creation")
class TestPositiveUserRegister:

    @allure.label("section2", "Positive")
    @allure.story("Successful registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_positive_create_user_successfully(self, api: UserApiClient):
        data = build_registration_body()
        api.register(data)
        api.response_status_code_should_be(200).response_json_should_have_key("id")


@allure.epic("User registration")
@allure.feature("User creation")
class TestNegativeUserRegister:

    @allure.label("section2", "Negative")
    @allure.story("Duplicate registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("negative")
    @pytest.mark.negative
    def test_negative_create_user_with_existing_email(self, api: UserApiClient):
        data = build_registration_body(EXISTING_USER_EMAIL)
        api.register(data)
        api.response_status_code_should_be(400)
        api.response_text_should_be(
            f"Users with email '{EXISTING_USER_EMAIL}' already exists"
        )

    @allure.label("section2", "Negative")
    @allure.story("Invalid data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "negative")
    @pytest.mark.negative
    def test_negative_create_user_with_invalid_email(self, api: UserApiClient):
        data = build_registration_body()
        data["email"] = "invalid.email.com"
        api.register(data)
        api.response_status_code_should_be(400)

    @allure.label("section2", "Negative")
    @allure.story("Missing required fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("validation", "negative")
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "missing_field",
        ["username", "firstName", "lastName", "email", "password"],
    )
    def test_negative_create_user_missing_field(
        self, api: UserApiClient, missing_field: str
    ):
        data = build_registration_body()
        del data[missing_field]
        api.register(data)
        api.response_status_code_should_be(400)
        api.response_text_should_contain("The following required params are missed")

    @allure.label("section2", "Negative")
    @allure.story("Validation - short name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "negative")
    @pytest.mark.negative
    def test_negative_create_user_with_short_name(self, api: UserApiClient):
        data = build_registration_body()
        data["firstName"] = "A"
        api.register(data)
        api.response_status_code_should_be(400)
        api.response_text_should_contain("The value of 'firstName' field is too short")

    @allure.label("section2", "Negative")
    @allure.story("Validation - long name")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("validation", "negative")
    @pytest.mark.negative
    def test_negative_create_user_with_long_name(self, api: UserApiClient):
        data = build_registration_body()
        data["firstName"] = "A" * 251
        api.register(data)
        api.response_status_code_should_be(400)
        api.response_text_should_contain("The value of 'firstName' field is too long")
