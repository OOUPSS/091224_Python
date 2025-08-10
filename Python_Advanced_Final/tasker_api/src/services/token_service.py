from uuid import UUID
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from src.repositories.token_repository import TokenRepository
from src.repositories.user_repository import UserRepository
from src.db.models import RefreshToken
from src.core.config import settings
from src.api.dependencies.token_dependency import create_access_token, create_refresh_token

class TokenService:
    def __init__(self, db: Session):
        self.db = db
        self.token_repository = TokenRepository()
        self.user_repository = UserRepository()

    def create_and_save_refresh_token(self, user_uuid: UUID) -> str:
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_refresh_token(
            data={"sub": str(user_uuid)}, expires_delta=refresh_token_expires
        )
        
        db_refresh_token = RefreshToken(
            token=refresh_token,
            user_uuid=user_uuid,
            expires_at=datetime.now(timezone.utc) + refresh_token_expires,
        )
        self.db.add(db_refresh_token)
        self.db.commit()
        self.db.refresh(db_refresh_token)
        return refresh_token

    def refresh_access_token(self, refresh_token: str) -> str:
        db_token = self.token_repository.get_refresh_token_by_token(self.db, refresh_token)
        
        if not db_token or db_token.used or db_token.expires_at < datetime.now(timezone.utc):
            raise ValueError("Invalid or expired refresh token")

        # Mark the old token as used and create a new one
        self.token_repository.mark_token_as_used(self.db, db_token)
        
        user = self.user_repository.get_by_uuid(self.db, db_token.user_uuid)
        if not user:
            raise ValueError("User not found")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return new_access_token