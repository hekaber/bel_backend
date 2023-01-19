from sqlalchemy import Column, Integer, String, Boolean
from ...dependencies.database.base_class import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(63), unique=True)
    email = Column(String(63), unique=True)
    phone = Column(String(63))
    mobile = Column(String(63))
    firstname = Column(String(63))
    lastname = Column(String(63))
    hash = Column(
            String(255), unique=True
            )
    salt = Column(String(255), unique=True)
    disabled = Column(Boolean)
