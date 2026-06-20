from datetime import datetime


def build_registration_body(email: str | None = None) -> dict:
    if email is None:
        stamp = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"learnqa{stamp}@example.com"
    return {
        "password": "123",
        "username": "learnqa",
        "firstName": "learnqa",
        "lastName": "learnqa",
        "email": email,
    }


DEFAULT_TEST_USER = {
    "email": "vinkotov@example.com",
    "password": "1234",
}
