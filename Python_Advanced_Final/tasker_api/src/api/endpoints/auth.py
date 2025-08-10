from datetime import timezone, datetime, timedelta
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from src.core.config import Settings
from src.db.database import get_db
from src.db.models import User, RefreshToken
from src.api.schemas import UserCreate, UserRead, TokenResponse, TokenData
from src.api.dependencies.token_dependency import create_access_token, create_refresh_token

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterUser(UserCreate):
    pass

class LoginUser(BaseModel):
    username: str
    password: str

@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: RegisterUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )
    
    new_user = User(**user_data.model_dump())
    new_user.uuid = uuid4()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@auth_router.post("/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    
    db_refresh_token = RefreshToken(
        token=refresh_token,
        user_uuid=user.uuid,
        expires_at=datetime.utcnow() + refresh_token_expires,
    )
    db.add(db_refresh_token)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}