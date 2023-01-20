from fastapi.security import OAuth2PasswordBearer
from fastapi import Header, HTTPException, Depends
from .utils.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_token_header(x_token: str = Header()):
    if x_token != 'my-x-token':
        raise HTTPException(status_code=400, detail="X-Token header invalid")