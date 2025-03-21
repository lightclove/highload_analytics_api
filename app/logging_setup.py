"""
Настройка централизованного логирования.
Гарантирует:
- Единый формат логов во всех модулях
- Контроль уровня детализации через конфиг
- Безопасность при многопоточной записи
"""
import logging
from .config import config

def setup_logging(name: str) -> logging.Logger:
    # Создаем логгер вместо использования root logger
    # для изоляции разных компонентов системы
    logger = logging.getLogger(name)
    
    # Устанавливаем уровень из конфига, а не хардкод
    logger.setLevel(config.LOG_LEVEL)
    
    # Форматирование с указанием имени модуля для фильтрации
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    
    # StreamHandler вместо FileHandler для Kubernetes-совместимости
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    # Предотвращение дублирования обработчиков
    if not logger.handlers:
        logger.addHandler(handler)
    
    # Отключаем propagation для избежания дублей
    logger.propagate = False
    
    return logger
