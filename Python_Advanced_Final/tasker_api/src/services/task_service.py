from uuid import UUID

from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.api.schemas import TaskCreate, TaskRead
from src.db.models import Task

class TaskService:
    def __init__(self, db: Session):
        self.repository = TaskRepository()
        self.db = db

    def create_task(self, task_data: TaskCreate, owner_uuid: UUID) -> Task:
        new_task = self.repository.create(self.db, task_data)
        new_task.owner_uuid = owner_uuid
        self.db.commit()
        return new_task

    def get_task_by_uuid(self, task_uuid: UUID) -> TaskRead:
        task = self.repository.get_by_uuid(self.db, task_uuid)
        return task

    def get_all_tasks(self) -> list[TaskRead]:
        tasks = self.repository.get_all(self.db)
        return tasks
        
    def get_tasks_by_owner(self, owner_uuid: UUID) -> list[TaskRead]:
        tasks = self.repository.get_tasks_by_owner_uuid(self.db, owner_uuid)
        return tasks

    def update_task(self, task: Task, task_data: TaskCreate) -> Task:
        updated_task = self.repository.update(self.db, task, task_data)
        return updated_task

    def delete_task(self, task: Task) -> Task:
        deleted_task = self.repository.remove(self.db, task)
        return deleted_task