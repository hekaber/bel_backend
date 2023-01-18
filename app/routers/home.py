from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..services.user import UserService
from ..dependencies import oauth2
from ..dependencies.exceptions.common import AuthenticationException
from ..dependencies.exceptions.user import UserNotFoundException
from ..models.schema.user import User, UserCreate


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
    return { "status": "test" }

@router.post(
        "/register",
        status_code=status.HTTP_201_CREATED
        )
def register_user(
    user: UserCreate,
    service: UserService = Depends()
    ):

    result = service.register_user(user)
    if not result["success"]:
        raise HTTPException(
                status_code=400,
                detail=result["message"]
                )
    return result

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends()):

    try:
        result = user_service.user_login(form_data.username, form_data.password)
    except UserNotFoundException as unfe:
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
    # user = User(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(
    #             status_code=400,
    #             detail="Incorrect username or password"
    #     )

    return {"access_token": user.username, "token_type": "bearer"}
