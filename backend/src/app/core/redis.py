import redis.asyncio as aioredis

from app.core.configs import settings

# Создаем асинхронный клиент Redis на основе URL из конфигурации
redis_client = aioredis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,  # Автоматически преобразует байты в строки
)


async def get_redis() -> aioredis.Redis:
    """Зависимость для внедрения Redis в эндпоинты (если потребуется)."""
    return redis_client