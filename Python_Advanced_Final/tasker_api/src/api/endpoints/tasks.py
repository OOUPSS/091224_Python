from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.api.schemas import TaskCreate, TaskRead
from src.api.dependencies.token_dependency import get_current_user
from src.api.dependencies.permission_dependency import Permission, PermissionChecker

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@task_router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db),
    permission: bool = Depends(PermissionChecker("task:create"))
):
    from src.db.models import Task
    
    new_task = Task(**task_data.model_dump())
    new_task.owner_uuid = current_user.uuid
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@task_router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db),
    permission: bool = Depends(PermissionChecker("task:read:any"))
):
    from src.db.models import Task
    
    task = db.query(Task).filter(Task.uuid == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not permission and task.owner_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not authorized to read this task")
        
    return task

@task_router.get("/", response_model=List[TaskRead])
def get_all_tasks(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Session = Depends(get_db),
    permission_any: bool = Depends(PermissionChecker("task:read:any")),
    permission_own: bool = Depends(PermissionChecker("task:read:own"))
):
    from src.db.models import Task

    if permission_any:
        return db.query(Task).all()
    elif permission_own:
        return db.query(Task).filter(Task.owner_uuid == current_user.uuid).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view tasks")