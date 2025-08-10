import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from src.main import app
from src.db.database import Base, get_db
from src.core.config import settings

# Новая переменная окружения для тестовой базы данных
TEST_DATABASE_URL = settings.APP_DB_URL.replace("fastapi_db", "test_db")
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