import binascii
import hashlib
import os
import jwt

from base64 import b64decode
from uuid import uuid4
from fastapi import Depends
from typing import List, Union

from ...models.orm import AccessKey
from ...models.schema.user import User
from ..database.db import get_db
from ...classes.config import config


def generate_token() -> str:
    return str(uuid4())

def generate_bearer_token(access_token: str) -> str:
    return jwt.encode(
        {
            "access_token":  access_token
        },
        b64decode(config("SECRET_KEY")),
        algorithm="HS256"
    )

def hash_password(password: str, salt: Union[bytes, None]=None) -> List[bytes]:

    salt = binascii.unhexlify(salt) if salt else os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return [key, salt]

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def decode_token(token: str, db = Depends(get_db)) -> dict:
    return jwt.decode(token, b64decode(config("SECRET_KEY")),"HS256")
