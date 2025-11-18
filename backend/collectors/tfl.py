import logging
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Dict
from typing import List

import requests
from models import TflMetric
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class TflCollector:
    BASE_URL = "https://api.tfl.gov.uk"

    def __init__(self):
        # TfL API no requiere API key para uso básico
        pass

    # ============================================================
    # 1. COLECTAR ESTADO DE LÍNEAS
    # ============================================================
    def collect_line_status(self, db: Session) -> List[TflMetric]:
        url = f"{self.BASE_URL}/Line/Mode/tube/Status"
        logger.info("Colectando estado de líneas TfL...")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            metrics: List[TflMetric] = []
            current_time = datetime.utcnow()
            two_minutes_ago = current_time - timedelta(minutes=2)

            for line in data:
                line_id = line.get("id", "")
                line_name = line.get("name", "")

                statuses = line.get("lineStatuses", [])
                if not statuses:
                    continue

                status = statuses[0]

                # ¿Ya existe dato reciente SIN cambio?
                existing = (
                    db.query(TflMetric)
                    .filter(
                        TflMetric.line_id == line_id,
                        TflMetric.date >= two_minutes_ago,
                    )
                    .first()
                )

                if existing and existing.status_severity == status.get(
                    "statusSeverity", 0
                ):
                    logger.info(f"Línea {line_name}: sin cambios, omitiendo.")
                    continue

                disruption = status.get("disruption") or {}

                tfl_metric = TflMetric(
                    date=current_time,
                    line_id=line_id,
                    line_name=line_name,
                    status_severity=status.get("statusSeverity", 0),
                    status_severity_description=status.get(
                        "statusSeverityDescription", "Unknown"
                    ),
                    reason=status.get("reason"),
                    disruption_category=disruption.get("category"),
                    closure_text=disruption.get("closureText"),
                )

                db.add(tfl_metric)
                metrics.append(tfl_metric)

                logger.info(
                    f"Guardando: {line_name} - {status.get('statusSeverityDescription')}"
                )

            if metrics:
                db.commit()
                for metric in metrics:
                    db.refresh(metric)

                logger.info(
                    f"Estado de {len(metrics)} líneas TfL guardado exitosamente"
                )
            else:
                logger.info("No hay cambios en líneas TfL.")

            return metrics

        except requests.exceptions.RequestException as e:
            logger.error(f"Error al colectar datos de TfL: {str(e)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            db.rollback()
            raise

    # ============================================================
    # 2. COLECTAR BIKE POINTS
    # ============================================================
    def collect_bike_points(self, db: Session, limit: int = 50) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/BikePoint"
        logger.info("Colectando información de BikePoints...")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            bike_points: List[Dict[str, Any]] = []

            for point in data[:limit]:
                bike_point = {
                    "id": point.get("id", ""),
                    "commonName": point.get("commonName", ""),
                    "lat": point.get("lat", 0),
                    "lon": point.get("lon", 0),
                    "bikes_available": 0,
                    "empty_docks": 0,
                    "total_docks": 0,
                }

                for prop in point.get("additionalProperties", []):
                    key = prop.get("key")
                    val = prop.get("value", "0")

                    if key == "NbBikes":
                        bike_point["bikes_available"] = int(val)
                    elif key == "NbEmptyDocks":
                        bike_point["empty_docks"] = int(val)
                    elif key == "NbDocks":
                        bike_point["total_docks"] = int(val)

                bike_points.append(bike_point)

            logger.info(f"Información de {len(bike_points)} BikePoints procesada")

            return {
                "total_points": len(data),
                "sample_size": len(bike_points),
                "bike_points": bike_points,
            }

        except Exception as e:
            logger.error(f"Error al colectar BikePoints: {str(e)}")
            raise

    # ============================================================
    # 3. COLECTAR ESTADO DE CARRETERAS
    # ============================================================
    def collect_road_status(
        self, db: Session, road_ids: List[str]
    ) -> List[Dict[str, Any]]:
        metrics: List[Dict[str, Any]] = []

        try:
            for road_id in road_ids:
                url = f"{self.BASE_URL}/Road/{road_id}/Status"

                logger.info(f"Colectando estado de la carretera: {road_id}")
                response = requests.get(url, timeout=15)
                response.raise_for_status()

                data = response.json()

                # TfL devuelve un array, no un objeto
                if isinstance(data, list) and len(data) > 0:
                    data = data[0]

                road_status = {
                    "id": data.get("id", road_id),
                    "displayName": data.get("displayName", ""),
                    "statusSeverity": data.get("statusSeverity", 0),
                    "statusSeverityDescription": data.get(
                        "statusSeverityDescription", ""
                    ),
                    "created": data.get("created", ""),
                    "modified": data.get("modified", ""),
                    "direction": data.get("direction", ""),
                    "closureText": data.get("closureText", ""),
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
