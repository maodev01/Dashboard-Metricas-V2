import requests
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from models import WeatherMetric
from config import settings

logger = logging.getLogger(__name__)

class WeatherCollector:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENWEATHER_API_KEY
        
    def collect_weather(self, db: Session, city: str = None, country: str = None) -> WeatherMetric:
        """
        Colecta datos del clima actual y los guarda en la base de datos
        """
        city = city or settings.DEFAULT_CITY
        country = country or settings.DEFAULT_COUNTRY
        
        try:
            params = {
                "q": f"{city},{country}",
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            logger.info(f"Colectando datos del clima para {city}, {country}")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Crear objeto WeatherMetric
            weather_metric = WeatherMetric(
                date=datetime.utcnow(),
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                pressure=data["main"]["pressure"],
                humidity=data["main"]["humidity"],
                weather_main=data["weather"][0]["main"],
                weather_description=data["weather"][0]["description"],
                wind_speed=data["wind"]["speed"],
                clouds=data["clouds"]["all"]
            )
            
            # Guardar en la base de datos
            db.add(weather_metric)
            db.commit()
            db.refresh(weather_metric)
            
            logger.info(f"Datos del clima guardados exitosamente. ID: {weather_metric.id}")
            return weather_metric
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al colectar datos del clima: {str(e)}")
            db.rollback()
            raise
        except KeyError as e:
            logger.error(f"Error al parsear respuesta de la API: {str(e)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            db.rollback()
            raise
    
    def collect_weather_by_coords(self, db: Session, lat: float = None, lon: float = None) -> WeatherMetric:
        """
        Colecta datos del clima usando coordenadas
        """
        lat = lat or settings.DEFAULT_LAT
        lon = lon or settings.DEFAULT_LON
        
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            logger.info(f"Colectando datos del clima para coordenadas: {lat}, {lon}")
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_metric = WeatherMetric(
                date=datetime.utcnow(),
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                temp_min=data["main"]["temp_min"],
                temp_max=data["main"]["temp_max"],
                pressure=data["main"]["pressure"],
                humidity=data["main"]["humidity"],
                weather_main=data["weather"][0]["main"],
                weather_description=data["weather"][0]["description"],
                wind_speed=data["wind"]["speed"],
                clouds=data["clouds"]["all"]
            )
            
            db.add(weather_metric)
            db.commit()
            db.refresh(weather_metric)
            
            logger.info(f"Datos del clima guardados exitosamente. ID: {weather_metric.id}")
            return weather_metric
            
        except Exception as e:
            logger.error(f"Error al colectar datos del clima por coordenadas: {str(e)}")
            db.rollback()
            raise