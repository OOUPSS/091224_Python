import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from src.main import app
from src.db.database import Base, get_db
from src.core.config import settings
from src.db.models import Permission, Role, User
from src.core.security import get_password_hash
from src.repositories.role_repository import RoleRepository
from src.services.permission_service import PermissionService

# Новая переменная окружения для тестовой базы данных
TEST_DATABASE_URL = "postgresql+psycopg2://admin_user:super_secret_pass@db_postgres:5432/test_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Создает и удаляет тестовую базу данных для каждого тестового сеанса.
    """
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)

def override_get_db():
    """
    Переопределяет зависимость базы данных для тестов.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client():
    """
    Фикстура для тестового клиента FastAPI.
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура для сеанса базы данных.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def permissions_and_roles(db_session):
    """
    Инициализирует права и роли для тестов.
    """
    permission_service = PermissionService(db_session)
    permission_service.initialize_permissions_and_roles()
    return db_session.query(Role).all()

@pytest.fixture(scope="module")
def test_user(db_session, permissions_and_roles):
    """
    Создает тестового пользователя с ролью 'user'.
    """
    role_repo = RoleRepository()
    user_role = role_repo.get_role_by_name(db_session, "user")
    
    user = User(
        username="test_user",
        email="test@example.com",
        password="test_password"
    )
    user.roles.append(user_role)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user