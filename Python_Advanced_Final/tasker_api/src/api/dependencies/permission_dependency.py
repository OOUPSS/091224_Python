from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from src.db.database import get_db
from src.db.models import User, Permission
from src.api.dependencies.token_dependency import get_current_user

def PermissionChecker(permission_name: str):
    def check_permission(
        db: Session = Depends(get_db),
        current_user: Annotated[dict, Depends(get_current_user)] = None
    ):
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
            
        user_permissions = set()
        for role in current_user.roles:
            user_permissions.update([p.name for p in role.permissions])
        
        if permission_name in user_permissions:
            return True
        
        raise HTTPException(status_code=403, detail="Not authorized")

    return check_permission