from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from src.db.models import Task
from src.api.schemas import TaskCreate, TaskRead
from .base_repository import BaseRepository

class TaskRepository(BaseRepository[Task, TaskCreate, TaskRead]):
    def __init__(self):
        super().__init__(Task)

    def get_tasks_by_owner_uuid(self, db: Session, owner_uuid: UUID) -> List[Task]:
        return db.query(self._model).filter(self._model.owner_uuid == owner_uuid).all()