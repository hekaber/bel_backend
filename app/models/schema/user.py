from typing import Union
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr


class User(BaseModel):
    username: Union[str, None] = None
    firstname: Union[str, None] = None
    lastname: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    mobile: Union[str, None] = None

    class Config:
        orm_mode = True

class UserCreate(User):
    password: Union[str, None] = None
    disabled: Union[bool, None] = None
