from typing import Type
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository

class UnitOfWork:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.users = UserRepository()
        self.tasks = TaskRepository()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.db_session.rollback()
        else:
            self.db_session.commit()

    def commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()

    @staticmethod
    def get_unit_of_work(db_session: Session = Depends(get_db)):
        return UnitOfWork(db_session)