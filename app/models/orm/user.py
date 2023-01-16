from sqlalchemy import Column, Integer, String, Boolean
from ...dependencies.database.db import Base

class UserOrm(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(63), unique=True)
    full_name = Column(String(63), unique=True)
    hashed_password = Column(
            String(63), unique=True
            )
    disabled = Column(Boolean)
