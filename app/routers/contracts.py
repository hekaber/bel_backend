from fastapi import APIRouter

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_contracts():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_contracts_me():
    return {"username": "fakecurrentuser"}


@router.get("/{contractaddress}")
async def read_contract(contractaddress: str):
    return {"contractaddress": contractaddress}