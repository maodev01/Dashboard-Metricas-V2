import requests
import logging
from datetime import datetime, date
from sqlalchemy.orm import Session
from models import NasaMetric
from config import settings

logger = logging.getLogger(__name__)

class NasaCollector:
    APOD_URL = "https://api.nasa.gov/planetary/apod"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.NASA_API_KEY
    
    def collect_apod(self, db: Session, apod_date: str = None) -> NasaMetric:
        """
        Colecta datos del Astronomy Picture of the Day (APOD)
        Si no se proporciona fecha, obtiene la imagen del día actual
        """
        try:
            params = {
                "api_key": self.api_key
            }
            
            if apod_date:
                params["date"] = apod_date
            
            logger.info(f"Colectando NASA APOD para fecha: {apod_date or 'hoy'}")
            response = requests.get(self.APOD_URL, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Crear objeto NasaMetric
            nasa_metric = NasaMetric(
                date=datetime.utcnow(),
                apod_date=data.get("date", str(date.today())),
                title=data.get("title", ""),
                explanation=data.get("explanation", ""),
                url=data.get("url", ""),
                hdurl=data.get("hdurl"),
                media_type=data.get("media_type", "image"),
                copyright=data.get("copyright")
            )
            
            # Guardar en la base de datos
            db.add(nasa_metric)
            db.commit()
            db.refresh(nasa_metric)
            
            logger.info(f"Datos de NASA APOD guardados exitosamente. ID: {nasa_metric.id}")
            return nasa_metric
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al colectar datos de NASA: {str(e)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            db.rollback()
            raise
    
    def collect_apod_range(self, db: Session, start_date: str, end_date: str) -> list[NasaMetric]:
        """
        Colecta múltiples APODs en un rango de fechas
        """
        try:
            params = {
                "api_key": self.api_key,
                "start_date": start_date,
                "end_date": end_date
            }
            
            logger.info(f"Colectando NASA APOD desde {start_date} hasta {end_date}")
            response = requests.get(self.APOD_URL, params=params, timeout=20)
            response.raise_for_status()
            
            data = response.json()
            
            # Si es una lista de resultados
            if isinstance(data, list):
                metrics = []
                for item in data:
                    nasa_metric = NasaMetric(
                        date=datetime.utcnow(),
                        apod_date=item.get("date", ""),
                        title=item.get("title", ""),
                        explanation=item.get("explanation", ""),
                        url=item.get("url", ""),
                        hdurl=item.get("hdurl"),
                        media_type=item.get("media_type", "image"),
                        copyright=item.get("copyright")
                    )
                    db.add(nasa_metric)
                    metrics.append(nasa_metric)
                
                db.commit()
                
                for metric in metrics:
                    db.refresh(metric)
                
                logger.info(f"{len(metrics)} registros de NASA APOD guardados exitosamente")
                return metrics
            else:
                # Si es un solo resultado
                return [self.collect_apod(db, data.get("date"))]
                
        except Exception as e:
            logger.error(f"Error al colectar rango de NASA APOD: {str(e)}")
            db.rollback()
            raise