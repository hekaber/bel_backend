import os

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies.oauth2 import get_current_access
from ..exceptions.user import UserException
from ..exceptions.auth import AuthenticationException
from ..services import AuthenticationService, UserService
from ..dependencies import oauth2
from ..models.schema.user import UserCreate
from ..models.orm.auth import AccessKey


router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root(token: str = Depends(oauth2.oauth2_scheme)):
    return {"token": token }

@router.get("/testing")
async def read_testing():
    return { "status": os.environ["SECRET_KEY"] }

# TODO: more secure, 1) email validation, 2) phone number
@router.post(
        "/register",
        status_code=status.HTTP_201_CREATED
        )
def register_user(
    user: UserCreate,
    service: UserService = Depends()
    ):
    result = service.create_user(user)
    if not result["success"]:
        raise HTTPException(
                status_code=400,
                detail=result["message"]
                )
    return result

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthenticationService = Depends()):

    try:
        result = service.user_login(form_data.username, form_data.password)
    except UserException as unfe:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=unfe.message
        )
    except AuthenticationException as ae:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ae.message
        )

    return result

@router.get("/logout")
async def logout(access_key: AccessKey = Depends(get_current_access), service: AuthenticationService = Depends()):
    if access_key:
        service.user_logout(access_key)

    return {
        "message": "logged out",
        "success": True
    }

@router.get("/token")
async def get_token():
     pass