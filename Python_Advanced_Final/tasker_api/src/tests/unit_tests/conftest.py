import pytest
from unittest.mock import MagicMock
from src.db.models import User, Task
from src.api.schemas import UserCreate, TaskCreate
from uuid import uuid4

@pytest.fixture
def mock_db_session():
    """
    Фикстура для создания мок-объекта сеанса базы данных.
    """
    return MagicMock()

@pytest.fixture
def mock_user_repository():
    """
    Фикстура для создания мок-объекта UserRepository.
    """
    return MagicMock()

@pytest.fixture
def mock_task_repository():
    """
    Фикстура для создания мок-объекта TaskRepository.
    """
    return MagicMock()

@pytest.fixture
def mock_role_repository():
    """
    Фикстура для создания мок-объекта RoleRepository.
    """
    return MagicMock()

@pytest.fixture
def test_user_data():
    """
    Фикстура для тестовых данных пользователя.
    """
    return UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="testpassword"
    )

@pytest.fixture
def test_task_data():
    """
    Фикстура для тестовых данных задачи.
    """
    return TaskCreate(
        title="Test Task",
        description="This is a test description."
    )

@pytest.fixture
def new_user():
    """
    Фикстура для создания мок-объекта пользователя.
    """
    user = User(
        username="newuser",
        email="newuser@example.com",
        password="newpassword"
    )
    user.uuid = uuid4()
    return user

@pytest.fixture
def new_task():
    """
    Фикстура для создания мок-объекта задачи.
    """
    task = Task(
        title="New Task",
        description="A task for testing."
    )
    task.uuid = uuid4()
    return task

@pytest.fixture
def mock_redis_client():
    """
    Фикстура для создания мок-объекта клиента Redis.
    """
    return MagicMock()