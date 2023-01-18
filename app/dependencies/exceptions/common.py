class AuthenticationException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "Invalid username or password."