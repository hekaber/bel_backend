from typing import Union
from .base import BaseRepository
from ..schema.user import UserCreate
from ..orm import User
from ...dependencies.utils.token import hash_password

class UserRepository(BaseRepository):

    def get_user_by_email(self, email: Union[str, None]):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserCreate):
        hashed_password, salt = hash_password(user.password)
        hash_to_store = hashed_password + salt
        user_dict = user.__dict__
        del user_dict['password']
        user_dict['hash'] = hash_to_store.hex()
        user_dict['salt'] = salt.hex()
        db_user = User(**user_dict)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user