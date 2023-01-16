from typing import Union
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from ..dependencies.database.db import Base
from pydantic import BaseModel, constr

class UserOrm(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(63), unique=True)
    full_name = Column(String(63), unique=True)
    hashed_password = Column(String(63), unique=True)
    disabled = Column(Boolean)

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    hashed_password: Union[str, None] = None

    class Config:
        orm_mode = True
