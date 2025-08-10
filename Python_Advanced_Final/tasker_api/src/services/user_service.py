from sqlalchemy.orm import Session
from src.repositories.user_repository import UserRepository
from src.repositories.role_repository import RoleRepository
from src.api.schemas import UserCreate
from src.db.models import User

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()

    def create_user(self, user_data: UserCreate) -> User:
        # Проверка на существование пользователя
        existing_user = self.user_repository.get_user_by_username(self.db, user_data.username)
        if existing_user:
            raise ValueError("Username already exists")
        
        existing_email = self.user_repository.get_user_by_email(self.db, user_data.email)
        if existing_email:
            raise ValueError("Email already exists")

        # Создание пользователя
        new_user = User(**user_data.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        # Назначение роли по умолчанию
        default_role = self.role_repository.get_role_by_name(self.db, "user")
        if default_role:
            new_user.roles.append(default_role)
            self.db.commit()
            self.db.refresh(new_user)

        return new_user