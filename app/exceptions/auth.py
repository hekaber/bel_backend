class AuthenticationException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "Invalid username or password."

class AuthenticationErrorException(AuthenticationException):
    def __init__(self, *args: object) -> None:
        self.message = "Server unable to decode tokens."
