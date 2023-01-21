from fastapi import Depends, HTTPException, status

from .oauth2 import oauth2_scheme
from .utils.token import decode_token
from ..models.schema.user import User
from ..models.orm.auth import AccessKey
from ..dependencies.database.db import get_db


async def get_current_access(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    data = decode_token(token, db)
    access_key = db.query(AccessKey).filter(AccessKey.access_token == data["access_token"]).first()
    if not access_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_key

# TODO: refactor this
async def get_current_active_user(current_user: User = Depends(get_current_access)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
