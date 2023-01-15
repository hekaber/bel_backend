from fastapi import FastAPI
from .routers import home, contracts, items, users

app = FastAPI()

app.include_router(contracts.router)
app.include_router(items.router)
app.include_router(home.router)
app.include_router(users.router)
