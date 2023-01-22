from fastapi.security import OAuth2PasswordBearer
from fastapi import Header, HTTPException, Depends, status

from .utils.token import decode_token
from ..dependencies.database.db import get_db
from ..models.orm import AccessKey

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

async def get_token_header(x_token: str = Header()):
    if x_token != 'my-x-token':
        raise HTTPException(status_code=400, detail="X-Token header invalid")