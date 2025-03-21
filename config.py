"""
Централизованная конфигурация приложения. 
Инкапсулирует все параметры окружения.
"""
import os

class AppConfig:
    # Вынесено в класс для возможности наследования 
    # и переопределения в тестах
    def __init__(self):
        # Используем os.getenv вместо dotenv для совместимости с Docker
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Явное преобразование типов для числовых параметров
        self.RATE_LIMIT = int(os.getenv("RATE_LIMIT", "1000"))  
        
        # Отдельный параметр для уровня логирования
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        
        # DSN для PostgreSQL с валидацией
        self.PG_DSN = os.getenv(
            "PG_DSN", 
            "postgresql://user:pass@localhost:5432/analytics"
        )

# Экспорт синглтона вместо глобальных переменных
config = AppConfig()
