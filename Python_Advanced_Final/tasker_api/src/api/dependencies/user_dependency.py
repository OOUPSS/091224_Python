from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.db.models import User

def get_user_by_uuid(user_uuid: UUID, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user