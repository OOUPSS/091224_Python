from uuid import uuid4, UUID
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from src.db.database import Base
from src.core.security import get_password_hash, verify_password

# Промежуточная таблица для связи User - Role
users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', UUID, ForeignKey('users.uuid'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

# Промежуточная таблица для связи Role - Permission
roles_permissions = Table(
    'roles_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")
    roles: Mapped[list["Role"]] = relationship(
        secondary=users_roles, back_populates="users"
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hashed_password = get_password_hash(password)
        
    def verify_password(self, password):
        return verify_password(password, self.hashed_password)

class Task(Base):
    __tablename__ = 'tasks'
    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    owner_uuid: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'))
    
    owner: Mapped["User"] = relationship(back_populates="tasks")

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    users: Mapped[list["User"]] = relationship(
        secondary=users_roles, back_populates="roles"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=roles_permissions, back_populates="roles"
    )

class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    roles: Mapped[list["Role"]] = relationship(
        secondary=roles_permissions, back_populates="permissions"
    )

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(200), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    user_uuid: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'))
    
    user: Mapped["User"] = relationship(back_populates="refresh_tokens")