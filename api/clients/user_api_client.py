from api.clients.base_api import BaseApi


class UserApiClient(BaseApi):
    def register(self, data: dict) -> "UserApiClient":
        return self.post("/user/", data=data)

    def login(self, email: str, password: str) -> "UserApiClient":
        return self.post("/user/login", data={"email": email, "password": password})

    def auth(self, token: str, auth_sid: str) -> "UserApiClient":
        return self.get(
            "/user/auth",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

    def get_user(
        self,
        user_id: int,
        token: str | None = None,
        auth_sid: str | None = None,
    ) -> "UserApiClient":
        headers: dict = {}
        cookies: dict = {}
        if token is not None:
            headers["x-csrf-token"] = token
        if auth_sid is not None:
            cookies["auth_sid"] = auth_sid
        return self.get(f"/user/{user_id}", headers=headers, cookies=cookies)

    def edit_user(
        self,
        user_id: int,
        data: dict,
        token: str | None = None,
        auth_sid: str | None = None,
    ) -> "UserApiClient":
        headers: dict = {}
        cookies: dict = {}
        if token is not None:
            headers["x-csrf-token"] = token
        if auth_sid is not None:
            cookies["auth_sid"] = auth_sid
        return self.put(f"/user/{user_id}", data=data, headers=headers, cookies=cookies)

    def delete_user(self, user_id: int, token: str, auth_sid: str) -> "UserApiClient":
        return self.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
