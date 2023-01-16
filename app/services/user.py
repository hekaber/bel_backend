from sqlalchemy.orm import Session
from app.models.repository.user import UserRepository
from ..models.schema.user import UserCreate
from fastapi import Depends


class UserService():

    def __init__(
            self,
            user_repository: UserRepository = Depends()
            ) -> None:
        self.user_repository = user_repository

    def register_user(self, user: UserCreate):
        user = self.user_repository.get_user_by_email(user)
        if user:
            return {
                "message": "User %s already exists".__format__(user.email),
                "content": user
            }

