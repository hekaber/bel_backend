from fastapi import APIRouter, Depends, HTTPException
from ..dependencies.user import get_current_user
from ..models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

