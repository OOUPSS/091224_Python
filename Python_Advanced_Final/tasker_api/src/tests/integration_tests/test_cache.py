import pytest
from fastapi import Depends
from redis.asyncio import Redis
from src.core.redis import get_redis_client

@pytest.mark.asyncio
async def test_redis_connection():
    """
    Тестирует подключение к Redis.
    """
    async for redis_client in get_redis_client():
        assert isinstance(redis_client, Redis)
        
        # Проверка, что клиент Redis работает
        await redis_client.set("test_key", "test_value")
        result = await redis_client.get("test_key")
        assert result == b"test_value"
        
        await redis_client.delete("test_key")
        result = await redis_client.get("test_key")
        assert result is None