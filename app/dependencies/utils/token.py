import binascii
import hashlib
import os
import jwt

from uuid import uuid4
from fastapi import Depends
from typing import List, Union

from ...models.orm.auth import AccessKey
from ...models.schema.user import User
from ..database.db import get_db

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def generate_secret(user: User) -> str:
    return f"{user.email}:{uuid4()}"

def generate_bearer_token(user: User, secret: str) -> str:
    return jwt.encode(
        {
            "username": user.username,
            "email": user.email,
        },
        secret,
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

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

def decode_token(token: str, db = Depends(get_db)):
    access_key = db.query(AccessKey).filter(AccessKey.access_token == token).first()
    return access_key.user if access_key else None
