import pytest
from uuid import uuid4
from src.services.task_service import TaskService
from src.api.schemas import TaskCreate

def test_create_task(mock_db_session, mock_task_repository):
    """
    Тестирует создание новой задачи.
    """
    task_service = TaskService(mock_db_session)
    task_data = TaskCreate(title="Test Task", description="Description")
    owner_uuid = uuid4()
    
    mock_task = MagicMock()
    mock_task_repository.create.return_value = mock_task
    task_service.repository = mock_task_repository
    
    task_service.create_task(task_data, owner_uuid)
    
    mock_task_repository.create.assert_called_once()
    mock_db_session.commit.assert_called_once()