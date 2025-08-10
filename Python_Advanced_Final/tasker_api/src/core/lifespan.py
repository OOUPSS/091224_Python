from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from redis.asyncio import Redis

from src.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Контекстный менеджер для управления жизненным циклом приложения FastAPI.
    """
    print("Application startup...")
    # Инициализация Redis
    app.state.redis = await Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    yield
    print("Application shutdown...")
    # Закрытие Redis
    await app.state.redis.close()