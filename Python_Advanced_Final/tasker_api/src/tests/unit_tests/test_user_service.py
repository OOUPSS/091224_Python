import pytest
from src.services.user_service import UserService
from src.api.schemas import UserCreate
from src.db.models import User
from unittest.mock import MagicMock

def test_create_user_success(mock_db_session, mock_user_repository, mock_role_repository, test_user_data):
    """
    Тестирует успешное создание пользователя.
    """
    mock_user_repository.get_user_by_username.return_value = None
    mock_user_repository.get_user_by_email.return_value = None
    
    mock_role = MagicMock()
    mock_role_repository.get_role_by_name.return_value = mock_role
    
    user_service = UserService(mock_db_session)
    user_service.user_repository = mock_user_repository
    user_service.role_repository = mock_role_repository
    
    user = user_service.create_user(test_user_data)
    
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    assert isinstance(user, User)

def test_create_user_existing_username(mock_db_session, mock_user_repository, test_user_data, new_user):
    """
    Тестирует создание пользователя с уже существующим именем.
    """
    mock_user_repository.get_user_by_username.return_value = new_user
    
    user_service = UserService(mock_db_session)
    user_service.user_repository = mock_user_repository
    
    with pytest.raises(ValueError):
        user_service.create_user(test_user_data)