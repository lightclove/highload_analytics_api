"""
Маршрутизация API.
Отвечает за:
- Валидацию входных данных
- Координацию сервисов
- Преобразование ошибок в HTTP-статусы
"""
from fastapi import APIRouter, Request, HTTPException
from .models import EventData
from .database import db_instance
from .redis_client import redis_client

router = APIRouter()

@router.post("/event", status_code=202)
async def create_event(request: Request):
    try:
        # Чтение тела запроса с обработкой ошибок парсинга
        data = await request.json()
    except ValueError:
        raise HTTPException(400, "Invalid JSON")
    
    try:
        # Валидация через конструктор модели
        event = EventData(
            user_id=data['user_id'],
            event_type=data['event_type'],
            timestamp=data['timestamp'],
            payload=data.get('payload', {})
        )
    except KeyError as e:
        # Точечная обработка ошибок отсутствия полей
        raise HTTPException(400, f"Missing required field: {e}")
    
    try:
        # Параллельное выполнение операций
        await asyncio.gather(
            redis_client.increment_counter(event.event_type),
            db_instance.save_event(event)
        )
        return {"status": "accepted"}
    except Exception as e:
        # Общий обработчик для изоляции ошибок инфраструктуры
        request.app.logger.error(f"Service error: {e}")
        raise HTTPException(500, "Internal server error")

@router.get("/stats/{event_type}")
async def get_stats(event_type: str):
    # Прямой доступ к кешу без бизнес-логики
    count = await redis_client.get_counter(event_type)
    return {"event_type": event_type, "count": count}
