from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

# --- Схемы для ролей и разрешений ---

class PermissionBase(BaseModel):
    name: str

class PermissionRead(PermissionBase):
    id: int
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str

class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead] = []
    class Config:
        from_attributes = True

# --- Схемы для пользователя ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    uuid: UUID
    roles: List[RoleRead] = []
    class Config:
        from_attributes = True

# --- Схемы для задач ---

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    uuid: UUID
    owner_uuid: UUID
    created_at: datetime
    class Config:
        from_attributes = True

# --- Схемы для токенов ---

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"