from base64 import b64decode
import binascii
import hashlib
import os
from uuid import uuid4
from ...models.schema.user import User
from typing import List, Union

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

def fake_hash_password(password: str):
    return "fakehashed" + password

def generate_access_token() -> str:
    return uuid4()

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
