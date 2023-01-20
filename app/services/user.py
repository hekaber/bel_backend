from sqlalchemy.exc import IntegrityError
from ..classes.enums import AuthType
from ..dependencies.utils.token import generate_bearer_token, generate_secret, hash_password
from ..exceptions import UserNotFoundException
from ..models.repository.user import UserRepository
from ..models.schema.user import User, UserCreate
from fastapi import Depends


class UserService():

    def __init__(
            self,
            user_repository: UserRepository = Depends()
            ) -> None:
        self.__user_repository = user_repository

    def create_user(self, user: UserCreate):
        existing_user = self.__user_repository.get_user_by_email_or_username(email=user.email, username=user.username)
        if existing_user:
            return {
                "message": f"User {user.email} already exists",
                "content": user,
                "success": False
            }
        try:
            result = self.__user_repository.create_user(user)
        except IntegrityError as ie:
            return {
                "message": f"Something failed in the database: {ie}",
                "content": {},
                "success": False
            }
        return {
            "message": f"User {result.username} created successfully",
            "content": User(**result.__dict__),
            "success": True
        }
