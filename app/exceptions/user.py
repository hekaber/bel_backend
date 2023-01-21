class UserException(Exception):
      pass

class UserNotFoundException(UserException):
        def __init__(self):
            self.message = "User not found"