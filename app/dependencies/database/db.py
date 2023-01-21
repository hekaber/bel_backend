from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...classes.config import config

SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
