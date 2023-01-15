from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=[""],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_root():
    return {"Hello": "World"}