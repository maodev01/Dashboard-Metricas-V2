from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from database import SessionLocal
from collectors.weather import WeatherCollector
from collectors.crypto import CryptoCollector
from collectors.nasa import NasaCollector
from config import settings
import logging

logger = logging.getLogger(__name__)

class MetricsScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.weather_collector = WeatherCollector()
        self.crypto_collector = CryptoCollector()
        self.nasa_collector = NasaCollector()
    
    def collect_all_metrics(self):
        """
        Colecta todas las métricas (clima, cripto, NASA)
        """
        db = SessionLocal()
        try:
            logger.info("Iniciando colección programada de métricas...")
            
            # Colectar datos del clima
            try:
                logger.info("Colectando datos del clima...")
                self.weather_collector.collect_weather(db)
                logger.info("✓ Datos del clima colectados")
            except Exception as e:
                logger.error(f"✗ Error colectando clima: {str(e)}")
            
            # Colectar datos de criptomonedas
            try:
                logger.info("Colectando datos de criptomonedas...")
                self.crypto_collector.collect_crypto(db)
                logger.info("✓ Datos de criptomonedas colectados")
            except Exception as e:
                logger.error(f"✗ Error colectando criptomonedas: {str(e)}")
            
            # Colectar datos de NASA
            try:
                logger.info("Colectando datos de NASA APOD...")
                self.nasa_collector.collect_apod(db)
                logger.info("✓ Datos de NASA colectados")
            except Exception as e:
                logger.error(f"✗ Error colectando NASA: {str(e)}")
            
            logger.info("Colección programada completada")
            
        except Exception as e:
            logger.error(f"Error general en colección programada: {str(e)}")
        finally:
            db.close()
    
    def start(self):
        """
        Inicia el scheduler con trabajos programados
        """
        # Programar colección diaria
        trigger = CronTrigger(
            hour=settings.COLLECTION_HOUR,
            minute=settings.COLLECTION_MINUTE,
            timezone='UTC'
        )
        
        self.scheduler.add_job(
            self.collect_all_metrics,
            trigger=trigger,
            id='daily_metrics_collection',
            name='Colección diaria de métricas',
            replace_existing=True
        )
        
        logger.info(f"Scheduler configurado para ejecutar a las {settings.COLLECTION_HOUR:02d}:{settings.COLLECTION_MINUTE:02d} UTC")
        
        # Iniciar el scheduler
        self.scheduler.start()
        logger.info("Scheduler iniciado exitosamente")
    
    def stop(self):
        """
        Detiene el scheduler
        """
        self.scheduler.shutdown()
        logger.info("Scheduler detenido")
    
    def run_now(self):
        """
        Ejecuta la colección de métricas inmediatamente (útil para testing)
        """
        logger.info("Ejecutando colección manual de métricas...")
        self.collect_all_metrics()

# Singleton del scheduler
metrics_scheduler = MetricsScheduler()