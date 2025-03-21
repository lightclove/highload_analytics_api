"""
Абстракция для работы с Redis.
Обеспечивает:
- Паттерн Unit of Work для pipeline
- Автоматическое управление подключениями
- Типизированный интерфейс
"""
from redis.asyncio import Redis
from .config import config

class RedisClient:
    def __init__(self):
        # Инкапсуляция состояния подключения
        self._client = None
    
    async def connect(self):
        # Подключение только при первом вызове
        if not self._client:
            # Используем StrictRedis-совместимый клиент
            self._client = Redis.from_url(
                config.REDIS_URL,
                decode_responses=True  # Автоматическая десериализация строк
            )
    
    async def disconnect(self):
        # Graceful shutdown
        if self._client:
            await self._client.close()
    
    async def increment_counter(self, event_type: str) -> int:
        # Pipeline для атомарности операций
        async with self._client.pipeline() as pipe:
            pipe.incr(f"events:{event_type}")
            pipe.expire(f"events:{event_type}", 86400)  # TTL 24 часа
            result = await pipe.execute()
            return result[0]  # Возвращаем новое значение счетчика
    
    async def get_counter(self, event_type: str) -> int:
        # Явное преобразование типа для защиты от None
        value = await self._client.get(f"events:{event_type}")
        return int(value) if value else 0

# Экспорт синглтона для повторного использования
redis_client = RedisClient()
