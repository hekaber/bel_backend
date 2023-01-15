from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .routers import home, contracts, items

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.include_router(contracts.router)
app.include_router(items.router)
app.include_router(home.router)
