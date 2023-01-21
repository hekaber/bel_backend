from fastapi import APIRouter, Depends
from ..dependencies.oauth2 import get_current_access


router = APIRouter(
    prefix="/certificates",
    tags=["certificates"],
    dependencies=[Depends(get_current_access)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_cert_list():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/generate")
async def get_cert_list():
    return {
        "status": "generated"
    }

@router.get("/{cert_uuid}")
async def get_cert(cert_uuid: str):
    return {"uuid": cert_uuid}