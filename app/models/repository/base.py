from ...dependencies.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


class BaseRepository():
    def __init__(
            self,
            db: Session = Depends(get_db)
            ) -> None:
        self.db = db
