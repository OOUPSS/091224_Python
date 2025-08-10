from sqlalchemy.orm import Session
from src.db.models import User
from src.api.schemas import UserCreate, UserRead
from .base_repository import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserRead]):
    def __init__(self):
        super().__init__(User)

    def get_user_by_username(self, db: Session, username: str) -> User:
        return db.query(self._model).filter(self._model.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> User:
        return db.query(self._model).filter(self._model.email == email).first()