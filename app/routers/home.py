from fastapi import Depends, APIRouter
from ..dependencies import oauth2

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