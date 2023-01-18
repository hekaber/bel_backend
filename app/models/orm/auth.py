from ...dependencies.database.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary

class AccessKey(Base):
    __tablename__ = 'access_key'
    id = Column(Integer, primary_key=True, nullable=False)

