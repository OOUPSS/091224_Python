import pytest
from src.services.rate_limiter import RateLimiterService
from unittest.mock import MagicMock
from redis.asyncio import Redis

@pytest.mark.asyncio
async def test_rate_limiter_check_rate_limit(mock_redis_client):
    """
    Тестирует логику ограничения частоты запросов.
    """
    rate_limiter = RateLimiterService(mock_redis_client)
    key = "test_rate_limit"
    limit = 5
    period = 60
    
    # Симулируем, что счетчик не превышает лимит
    mock_redis_client.pipeline.return_value.execute.return_value = [3, None]
    is_allowed = await rate_limiter.check_rate_limit(key, limit, period)
    assert is_allowed is True
    
    # Симулируем, что счетчик превышает лимит
    mock_redis_client.pipeline.return_value.execute.return_value = [6, None]
    is_allowed = await rate_limiter.check_rate_limit(key, limit, period)
    assert is_allowed is False