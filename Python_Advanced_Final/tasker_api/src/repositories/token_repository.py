from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from src.db.models import RefreshToken
from src.api.schemas import TokenResponse
from .base_repository import BaseRepository

class TokenRepository(BaseRepository[RefreshToken, None, None]):
    def __init__(self):
        super().__init__(RefreshToken)

    def get_refresh_token_by_token(self, db: Session, token: str) -> RefreshToken:
        return db.query(self._model).filter(self._model.token == token).first()

    def mark_token_as_used(self, db: Session, token: RefreshToken) -> RefreshToken:
        token.used = True
        token.used_at = datetime.now(timezone.utc)
        db.add(token)
        db.commit()
        db.refresh(token)
        return token