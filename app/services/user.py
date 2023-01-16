from sqlalchemy.orm import Session
from ..models.orm.user import UserCreate

class UserService():

    def create_user(db: Session, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

