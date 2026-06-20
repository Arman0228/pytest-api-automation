from dataclasses import dataclass


@dataclass
class AuthSession:
    auth_sid: str
    token: str
    user_id: int
