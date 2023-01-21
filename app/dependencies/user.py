from fastapi import Depends, HTTPException

from ..models.schema.user import User
from .oauth2 import get_current_access

# TODO: refactor this
async def get_current_active_user(current_user: User = Depends(get_current_access)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
