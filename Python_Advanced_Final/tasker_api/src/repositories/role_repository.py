from sqlalchemy.orm import Session
from src.db.models import Role
from .base_repository import BaseRepository

class RoleRepository(BaseRepository[Role, None, None]):
    def __init__(self):
        super().__init__(Role)

    def get_role_by_name(self, db: Session, name: str) -> Role:
        return db.query(self._model).filter(self._model.name == name).first()