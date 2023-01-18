from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies.user import get_current_active_user
from ..services import UserService
from ..models.schema.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

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
