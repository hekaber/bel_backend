from base64 import b64encode
import binascii
from typing import Union
from .base import BaseRepository
from sqlalchemy import or_
from ..schema.user import UserCreate
from ..orm import User
from ...dependencies.utils.token import hash_password

class UserRepository(BaseRepository):

    def get_user_by_email_or_username(self, email: Union[str, None]=None, username: Union[str, None]=None):
        """ Get user by email or username criteria"""
        return self.db.query(User).filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()

    def create_user(self, user: UserCreate):
        hashed_password, salt = hash_password(user.password)
        hash_to_store = hashed_password + salt
        user_dict = user.__dict__
        del user_dict['password']
        user_dict['hash'] = binascii.hexlify(hash_to_store)
        user_dict['salt'] = binascii.hexlify(salt)
        db_user = User(**user.__dict__)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user