"""
Ядро приложения. Отвечает за:
- Инициализацию компонентов
- Регистрацию middleware и роутов
- Управление жизненным циклом
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import router
from .database import db_instance
from .redis_client import redis_client
from .logging_setup import setup_logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация в правильном порядке
    logger = setup_logger(__name__)
    logger.info("Starting service")
    
    try:
        await db_instance.connect()
        await redis_client.connect()
        yield
    finally:
        # Гарантированная очистка ресурсов
        await db_instance.disconnect()
        await redis_client.disconnect()
        logger.info("Service stopped")

app = FastAPI(lifespan=lifespan)

# Регистрация компонентов
app.include_router(router, prefix="/api/v1")

# Добавление middleware для CORS, GZip и пр.
# app.add_middleware(...)
