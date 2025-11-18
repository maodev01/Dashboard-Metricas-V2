from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database import SessionLocal
from collectors.weather import WeatherCollector
from collectors.crypto import CryptoCollector
from collectors.tfl import TflCollector
from config import settings
import logging

logger = logging.getLogger(__name__)


class MetricsScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.weather_collector = WeatherCollector()
        self.crypto_collector = CryptoCollector()
        self.tfl_collector = TflCollector()

    def collect_all_metrics(self):
        """
        Colecta todas las métricas (clima, cripto, TfL)
        """
        db = SessionLocal()
        try:
            logger.info("🔄 Iniciando colección automática de métricas...")

            # Colectar datos del clima
            try:
                logger.info("🌤️ Colectando datos del clima...")
                self.weather_collector.collect_weather(db)
                logger.info("✅ Datos del clima colectados")
            except Exception as e:
                logger.error(f"❌ Error colectando clima: {str(e)}")

            # Colectar datos de criptomonedas
            try:
                logger.info("💰 Colectando datos de criptomonedas...")
                self.crypto_collector.collect_crypto(db)
                logger.info("✅ Datos de criptomonedas colectados")
            except Exception as e:
                logger.error(f"❌ Error colectando criptomonedas: {str(e)}")

            # Colectar datos de TfL
            try:
                logger.info("🚇 Colectando estado de TfL...")
                self.tfl_collector.collect_line_status(db)
                logger.info("✅ Datos de TfL colectados")
            except Exception as e:
                logger.error(f"❌ Error colectando TfL: {str(e)}")

            logger.info("✅ Colección automática completada")

        except Exception as e:
            logger.error(f"❌ Error general en colección: {str(e)}")
        finally:
            db.close()

    def start(self):
        """
        Inicia el scheduler con colección cada N minutos
        """
        # Programar colección cada X minutos
        trigger = IntervalTrigger(minutes=settings.COLLECTION_INTERVAL_MINUTES)

        self.scheduler.add_job(
            self.collect_all_metrics,
            trigger=trigger,
            id='periodic_metrics_collection',
            name=f'Colección de métricas cada {settings.COLLECTION_INTERVAL_MINUTES} minutos',
            replace_existing=True
        )

        logger.info(
            f"⏰ Scheduler configurado para ejecutar cada {settings.COLLECTION_INTERVAL_MINUTES} minutos")

        # Ejecutar una colección inicial inmediata
        logger.info("🚀 Ejecutando colección inicial...")
        self.collect_all_metrics()

        # Iniciar el scheduler
        self.scheduler.start()
        logger.info("✅ Scheduler iniciado exitosamente")

    def stop(self):
        """
        Detiene el scheduler
        """
        self.scheduler.shutdown()
        logger.info("🛑 Scheduler detenido")

    def run_now(self):
        """
        Ejecuta la colección de métricas inmediatamente
        """
        logger.info("▶️ Ejecutando colección manual de métricas...")
        self.collect_all_metrics()


# Singleton del scheduler
metrics_scheduler = MetricsScheduler()
