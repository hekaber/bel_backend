from base64 import b64encode
import binascii
from typing import Union
from .base import BaseRepository
from sqlalchemy import or_, text, insert
from ..schema.user import UserCreate
from ..orm import User
from ...dependencies.utils.token import hash_password
from ...classes.enums import AuthType
from ...models.orm.auth import AccessKey


class UserRepository(BaseRepository):

    def get_user_by_email_or_username(
            self,
            email: Union[str, None]=None,
            username: Union[str, None]=None
            ) -> Union[User, None]:
        """ Get user by email or username criteria"""
        return self.db.query(User).filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()

    def create_user(self, user: UserCreate) -> User:
        """Create new user in system"""
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

    def upsert_token(self, user: User, access_token: str) -> None:
        """Update/Insert any kind of token"""
        existing_key = self.db.query(AccessKey).filter(
                AccessKey.user_id == user.id,
                AccessKey.auth_type == AuthType.BEARER.value
                ).first()

        if existing_key:
            self.db.query(
                    AccessKey
                    ).filter(
                    AccessKey.id == existing_key.id
                    ).update({'access_token': access_token})
        else:
            db_access_key = AccessKey(
                user=user,
                access_token=access_token,
                auth_type=AuthType.BEARER.value
                )
            self.db.add(db_access_key)
        self.db.commit()

    def get_access_key(self, user: User, auth_type: str) -> AccessKey:
        """Access authentication"""
        return self.db.query(AccessKey).filter(
            AccessKey.user_id == user.id,
            AccessKey.auth_type == auth_type
        ).first()
