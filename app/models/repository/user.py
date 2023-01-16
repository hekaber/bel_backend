from typing import Union
from .base import BaseRepository
from ..schema.user import UserCreate
from ..orm import UserOrm


class UserRepository(BaseRepository):

    def get_user_by_email(self, email: Union[str, None]):
        self.db.query(UserOrm).filter(UserOrm.email == email).first()

    def create_user(self, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = UserOrm(email=user.email, hashed_password=fake_hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user