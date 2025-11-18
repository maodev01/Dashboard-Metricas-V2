import requests
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import TflMetric

logger = logging.getLogger(__name__)


class TflCollector:
    BASE_URL = "https://api.tfl.gov.uk"

    def __init__(self):
        # TfL API no requiere API key para uso básico
        pass

    def collect_line_status(self, db: Session) -> list[TflMetric]:

        try:
            url = f"{self.BASE_URL}/Line/Mode/tube/Status"
            logger.info("Colectando estado de líneas TfL...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            metrics = []
            current_time = datetime.utcnow()
            two_minutes_ago = current_time - timedelta(minutes=2)
            for line in data:
                line_id = line.get("id", "")
                line_name = line.get("name", "")
                # Obtener primer estado (usualmente el actual)
                line_statuses = line.get("lineStatuses", [])
                if not line_statuses:
                    continue
                status = line_statuses[0]
                # Verificar si ya existe un registro muy reciente (últimos 2 minutos)
                existing = db.query(TflMetric).filter(
                    TflMetric.line_id == line_id,
                    TflMetric.date >= two_minutes_ago
                ).first()
                # Si existe un registro reciente y el estado no cambió, skip
                if existing and existing.status_severity == status.get("statusSeverity", 0):
                    logger.info(f"Línea {line_name}: Sin cambios, omitiendo")
                    continue
                # Extraer información de disrupciones si existen
                disruption = status.get("disruption", {}) if status.get(
                    "disruption") else {}
                tfl_metric = TflMetric(
                    date=current_time,
                    line_id=line_id,
                    line_name=line_name,
                    status_severity=status.get("statusSeverity", 0),
                    status_severity_description=status.get(
                        "statusSeverityDescription", "Unknown"),
                    reason=status.get("reason"),
                    disruption_category=disruption.get(
                        "category") if disruption else None,
                    closure_text=disruption.get(
                        "closureText") if disruption else None
                )
                db.add(tfl_metric)
                metrics.append(tfl_metric)
                logger.info(
                    f"Guardando: {line_name} - {status.get('statusSeverityDescription')}")
            if metrics:
                db.commit()
                for metric in metrics:
                    db.refresh(metric)
                logger.info(
                    f"Estado de {len(metrics)} líneas TfL guardado exitosamente")
            else:
                logger.info("No hay cambios en las líneas TfL")
            return metrics
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al colectar datos de TfL: {str(e)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            db.rollback()
            raise

    def collect_bike_points(self, db: Session, limit: int = 50) -> dict:
        """
        Colecta información de puntos de bicicletas (BikePoints)
        Retorna un resumen, no lo guarda en DB para evitar sobrecarga
        """
        try:
            url = f"{self.BASE_URL}/BikePoint"

            logger.info(f"Colectando información de BikePoints...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Procesar solo los primeros N puntos
            bike_points = []
            for point in data[:limit]:
                bike_point = {
                    "id": point.get("id", ""),
                    "commonName": point.get("commonName", ""),
                    "lat": point.get("lat", 0),
                    "lon": point.get("lon", 0),
                    "bikes_available": 0,
                    "empty_docks": 0,
                    "total_docks": 0
                }

                # Extraer propiedades adicionales
                additional_props = point.get("additionalProperties", [])
                for prop in additional_props:
                    key = prop.get("key", "")
                    value = prop.get("value", "0")

                    if key == "NbBikes":
                        bike_point["bikes_available"] = int(value)
                    elif key == "NbEmptyDocks":
                        bike_point["empty_docks"] = int(value)
                    elif key == "NbDocks":
                        bike_point["total_docks"] = int(value)

                bike_points.append(bike_point)

            logger.info(
                f"Información de {len(bike_points)} BikePoints procesada")
            return {
                "total_points": len(data),
                "sample_size": len(bike_points),
                "bike_points": bike_points
            }

        except Exception as e:
            logger.error(f"Error al colectar BikePoints: {str(e)}")
            raise

    def collect_road_status(self, db: Session, road_ids: list) -> list[dict]:
        """
        Colecta el estado de carreteras específicas por sus IDs
        Retorna una lista de diccionarios con el estado de cada carretera
        """
        try:
            metrics = []
            for road_id in road_ids:
                url = f"{self.BASE_URL}/Road/{road_id}/Status"

                logger.info(f"Colectando estado de la carretera: {road_id}")
                response = requests.get(url, timeout=15)
                response.raise_for_status()

                data = response.json()

                road_status = {
                    "id": data.get("id", ""),
                    "displayName": data.get("displayName", ""),
                    "statusSeverity": data.get("statusSeverity", 0),
                    "statusSeverityDescription": data.get("statusSeverityDescription", ""),
                    "created": data.get("created", ""),
                    "modified": data.get("modified", ""),
                    "direction": data.get("direction", ""),
                    "closureText": data.get("closureText", "")
                }

                metrics.append(road_status)
                logger.info(f"Estado de la carretera {road_id} colectado")

            return metrics

        except requests.exceptions.RequestException as e:
            logger.error(f"Error al colectar estado de carreteras: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            raise
