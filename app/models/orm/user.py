from sqlalchemy import Column, Integer, String, Boolean
from ...dependencies.database.db import declarative_base


Base = declarative_base()

class UserOrm(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(63), unique=True)
    email = Column(String(63), unique=True)
    firstname = Column(String(63), unique=True)
    lastname = Column(String(63), unique=True)
    hashed_password = Column(
            String(63), unique=True
            )
    disabled = Column(Boolean)
