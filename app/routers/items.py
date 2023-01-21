from fastapi import APIRouter, Depends
from typing import Union

from ..dependencies.user import get_current_access
from ..dependencies.oauth2 import get_token_header


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[
        Depends(get_token_header),
        Depends(get_current_access)
    ],
    responses={404: {"description": "Not found"}},
)

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
