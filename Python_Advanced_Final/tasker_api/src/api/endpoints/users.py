from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.api.schemas import UserRead
from src.api.dependencies.token_dependency import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/me", response_model=UserRead)
def read_current_user(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user