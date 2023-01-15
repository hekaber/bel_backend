from fastapi import FastAPI
from .routers import home, contracts, items

app = FastAPI()

app.include_router(contracts.router)
app.include_router(items.router)
app.include_router(home.router)
