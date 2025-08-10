from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.db.models import Task

def get_task_by_id(task_id: UUID, db: Session = Depends(get_db)) -> Task:
    task = db.query(Task).filter(Task.uuid == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task