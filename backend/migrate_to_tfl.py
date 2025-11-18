"""
Script de migración: NASA → TfL
Elimina tabla nasa_metrics y crea tabla tfl_metrics
"""

from database import engine, Base
from models import TflMetric
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    try:
        # Eliminar tabla nasa_metrics si existe
        logger.info("Eliminando tabla nasa_metrics...")
        Base.metadata.reflect(bind=engine)
        if "nasa_metrics" in Base.metadata.tables:
            Base.metadata.tables["nasa_metrics"].drop(engine)
            logger.info("✅ Tabla nasa_metrics eliminada")
        else:
            logger.info("ℹ️  Tabla nasa_metrics no existe")

        # Crear nueva tabla tfl_metrics
        logger.info("Creando tabla tfl_metrics...")
        TflMetric.__table__.create(engine, checkfirst=True)
        logger.info("✅ Tabla tfl_metrics creada")

        logger.info("🎉 Migración completada exitosamente")

    except Exception as e:
        logger.error(f"❌ Error en migración: {str(e)}")
        raise


if __name__ == "__main__":
    migrate()
