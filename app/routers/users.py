from fastapi import APIRouter, Depends, HTTPException
from ..dependencies.user import get_current_active_user
from ..services import UserService
from ..models.schema.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/register")
def register_user(
    user: User,
    service: UserService = Depends()
    ):
    registered = service.register_user(user)
