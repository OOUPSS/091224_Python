from typing import AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis

from src.core.lifespan import lifespan

async def get_redis_client() -> AsyncGenerator[Redis, None]:
    """
    Зависимость для получения клиента Redis.
    """
    async with lifespan():
        redis_client = await Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        yield redis_client