from fastapi import Depends, HTTPException, status
from .oauth2 import oauth2_scheme
from .utils.token import decode_token
from ..models.schema.user import User
from ..dependencies.database.db import get_db


async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    user = decode_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
