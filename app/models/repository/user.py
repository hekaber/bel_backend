from typing import Union
from .base import BaseRepository
from ..schema.user import UserCreate
from ..orm import User


class UserRepository(BaseRepository):

    def get_user_by_email(self, email: Union[str, None]):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        hashed_password = user.password
        user_dict = user.__dict__
        del user_dict['password']
        db_user = User(**user_dict)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user