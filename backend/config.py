from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./metrics.db"

    # API Keys (todas gratuitas y abiertas)
    # Obtener en https://openweathermap.org/api
    OPENWEATHER_API_KEY: Optional[str] = None

    # Configuración de la aplicación
    APP_NAME: str = "Dashboard de Métricas"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: list = ["*"]

    # Ubicación por defecto
    DEFAULT_CITY: str = "Bucaramanga"
    DEFAULT_COUNTRY: str = "CO"
    DEFAULT_LAT: float = 7.1254
    DEFAULT_LON: float = -73.1198

    # Configuración de scheduler
    COLLECTION_INTERVAL_MINUTES: int = 5  # Intervalo de colecta de métricas

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
