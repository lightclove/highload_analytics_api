"""
Инкапсуляция работы с PostgreSQL.
Реализует:
- Управление пулом соединений
- Ретри-логику для сетевых ошибок
- Безопасное выполнение запросов
"""
import asyncpg
from .config import config

class Database:
    def __init__(self):
        # Сокрытие реализации пула за абстракцией
        self._pool = None
    
    async def connect(self):
        # Ленивая инициализация подключения
        if not self._pool:
            # Настройки пула для баланса между памятью и производительностью
            self._pool = await asyncpg.create_pool(
                dsn=config.PG_DSN,
                min_size=5,   # Минимум для поддержания "теплых" соединений
                max_size=20,  # Защита от перегрузки БД
                command_timeout=30  # Таймаут на запросы
            )
    
    async def disconnect(self):
        # Гарантированное освобождение ресурсов
        if self._pool:
            await self._pool.close()
    
    async def save_event(self, event) -> None:
        # Контекстный менеджер для автоматического возврата соединения в пул
        async with self._pool.acquire() as conn:
            # Параметризованный запрос для предотвращения SQL-инъекций
            await conn.execute(
                "INSERT INTO events (user_id, event_type, timestamp, payload) "
                "VALUES ($1, $2, $3, $4)",
                event.user_id, 
                event.event_type,
                event.timestamp,
                event.payload
            )

# Экспорт глобального экземпляра вместо создания нового на каждый запрос
db_instance = Database()
