from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..dependencies import oauth2
from ..dependencies.utils.token import fake_users_db, fake_hash_password
from ..models import User


router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root(token: str = Depends(oauth2.oauth2_scheme)):
    return {"token": token }

@router.get("/testing")
async def read_testing(token: str = Depends(oauth2.oauth2_scheme)):
    return {"token": token, "status": "test" }

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
                status_code=400,
                detail="Incorrect username or password"
        )
    user = User(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
                status_code=400,
                detail="Incorrect username or password"
        )

    return {"access_token": user.username, "token_type": "bearer"}
