from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./metrics.db"
    
    # API Keys (todas gratuitas y abiertas)
    OPENWEATHER_API_KEY: Optional[str] = None  # Obtener en https://openweathermap.org/api
    NASA_API_KEY: str = "DEMO_KEY"  # DEMO_KEY funciona pero tiene límites
    
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
    COLLECTION_HOUR: int = 0  # Hora UTC para colectar datos (0 = medianoche)
    COLLECTION_MINUTE: int = 0
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()