import time
from typing import Optional
from redis.asyncio import Redis

class RateLimiterService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def check_rate_limit(self, key: str, limit: int, period: int) -> bool:
        """
        Проверяет и обновляет счетчик запросов для заданного ключа.
        Возвращает True, если запрос разрешен, и False, если превышен лимит.
        """
        pipe = self.redis_client.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, period)
        current_count = await pipe.execute()
        
        return current_count[0] <= limit