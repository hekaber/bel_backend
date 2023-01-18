from sqlalchemy.exc import IntegrityError
from app.models.repository.user import UserRepository
from ..models.schema.user import User, UserCreate
from fastapi import Depends


class UserService():

    def __init__(
            self,
            user_repository: UserRepository = Depends()
            ) -> None:
        self.user_repository = user_repository

    def register_user(self, user: UserCreate):
        existing_user = self.user_repository.get_user_by_email(user.email)
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
