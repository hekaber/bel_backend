from fastapi import FastAPI
from .routers import home, contracts, items, users
from .models import orm
from .dependencies.database.db import engine
from dotenv import load_dotenv

orm.user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contracts.router)
app.include_router(items.router)
app.include_router(home.router)
app.include_router(users.router)
