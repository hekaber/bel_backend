from typing import Union
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    hashed_password: Union[str, None] = None

    class Config:
        orm_mode = True

class UserCreate(User):
    password: Union[str, None] = None
