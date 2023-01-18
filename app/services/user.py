import binascii
from sqlalchemy.exc import IntegrityError
from ..dependencies.exceptions.common import AuthenticationException
from ..dependencies.utils.token import generate_access_token, hash_password
from ..dependencies.exceptions.user import UserNotFoundException
from ..models.repository.user import UserRepository
from ..models.schema.user import User, UserCreate
from fastapi import Depends


class UserService():

    def __init__(
            self,
            user_repository: UserRepository = Depends()
            ) -> None:
        self.user_repository = user_repository

    def user_login(self, username: str, password: str) -> dict:
        user = self.user_repository.get_user_by_email_or_username(username=username)
        if user is None:
            raise UserNotFoundException()

        check_hash, salt = hash_password(password, user.salt)

        if check_hash != binascii.unhexlify(user.hash)[:32]:
            raise AuthenticationException()

        if user.access_token:
            return {
            "message": "authentified",
                "content": {
                    "token": user.access_token,
                    "token_type": "Bearer"
                },
                "success": True
            }

        access_token = generate_access_token()
        user.access_token = access_token
        user = self.user_repository.update_token(user, access_token)
        return {
            "message": "authentified",
            "content": {
                "token": access_token,
                "token_type": "Bearer"
            },
            "success": True
        }

    def register_user(self, user: UserCreate):
        existing_user = self.user_repository.get_user_by_email_or_username(email=user.email, username=user.username)
        if existing_user:
            return {
                "message": f"User {user.email} already exists",
                "content": user,
                "success": False
            }
        try:
            result = self.user_repository.create_user(user)
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
