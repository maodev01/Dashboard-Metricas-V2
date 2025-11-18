# backend/routes.py
import logging

from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from collectors.crypto import CryptoCollector
from collectors.tfl import TflCollector
from collectors.weather import WeatherCollector
from database import get_db
from models import CryptoMetric, TflMetric, WeatherMetric

logger = logging.getLogger(__name__)

router = APIRouter()

# ==================== WEATHER ENDPOINTS ====================


@router.get("/weather/latest")
async def get_latest_weather(db: Session = Depends(get_db)):
    """Obtiene el registro más reciente del clima"""
    weather = db.query(WeatherMetric).order_by(WeatherMetric.date.desc()).first()
    if not weather:
        raise HTTPException(status_code=404, detail="No weather data found")
    return weather.to_dict()


@router.get("/weather/daily")
async def get_daily_weather(
    target_date: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Obtiene datos del clima para un día específico"""
    if target_date:
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
            )
    else:
        parsed_date = date.today()

    # Buscar registros del día específico
    weather = (
        db.query(WeatherMetric)
        .filter(func.date(WeatherMetric.date) == parsed_date)
        .order_by(WeatherMetric.date.desc())
        .first()
    )

    if not weather:
        raise HTTPException(
            status_code=404, detail=f"No weather data found for {parsed_date}"
        )

    return weather.to_dict()


@router.get("/weather/range")
async def get_weather_range(
    start_date: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha final YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """Obtiene datos del clima en un rango de fechas"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    if end < start:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    weather_data = (
        db.query(WeatherMetric)
        .filter(and_(WeatherMetric.date >= start, WeatherMetric.date <= end))
        .order_by(WeatherMetric.date.asc())
        .all()
    )

    return [w.to_dict() for w in weather_data]


@router.post("/weather/collect")
async def collect_weather_now(
    city: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Colecta datos del clima inmediatamente"""
    try:
        collector = WeatherCollector()
        weather = collector.collect_weather(db, city, country)
        return {
            "message": "Weather data collected successfully",
            "data": weather.to_dict(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error collecting weather data: {str(e)}"
        )


# ==================== CRYPTO ENDPOINTS ====================


@router.get("/crypto/latest")
async def get_latest_crypto(db: Session = Depends(get_db)):
    from sqlalchemy import func

    # Subconsulta para obtener la fecha máxima por símbolo
    subquery = (
        db.query(CryptoMetric.symbol, func.max(CryptoMetric.date).label("max_date"))
        .group_by(CryptoMetric.symbol)
        .subquery()
    )

    # Unir con la tabla principal para obtener los registros más recientes
    cryptos = (
        db.query(CryptoMetric)
        .join(
            subquery,
            and_(
                CryptoMetric.symbol == subquery.c.symbol,
                CryptoMetric.date == subquery.c.max_date,
            ),
        )
        .order_by(CryptoMetric.market_cap_rank.asc())
        .limit(6)
        .all()
    )

    if not cryptos:
        raise HTTPException(status_code=404, detail="No crypto data found")

    return [c.to_dict() for c in cryptos]


@router.get("/crypto/daily")
async def get_daily_crypto(
    target_date: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    symbol: Optional[str] = Query(
        None, description="Símbolo de la criptomoneda (BTC, ETH, etc.)"
    ),
    db: Session = Depends(get_db),
):
    """Obtiene datos de criptomonedas para un día específico"""
    if target_date:
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
            )
    else:
        parsed_date = date.today()

    query = db.query(CryptoMetric).filter(func.date(CryptoMetric.date) == parsed_date)

    if symbol:
        query = query.filter(CryptoMetric.symbol == symbol.upper())

    cryptos = query.order_by(CryptoMetric.market_cap_rank.asc()).all()

    if not cryptos:
        raise HTTPException(
            status_code=404, detail=f"No crypto data found for {parsed_date}"
        )

    return [c.to_dict() for c in cryptos]


@router.get("/crypto/range")
async def get_crypto_range(
    start_date: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha final YYYY-MM-DD"),
    symbol: Optional[str] = Query(None, description="Símbolo de la criptomoneda"),
    db: Session = Depends(get_db),
):
    """Obtiene datos de criptomonedas en un rango de fechas"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    if end < start:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    query = db.query(CryptoMetric).filter(
        and_(CryptoMetric.date >= start, CryptoMetric.date <= end)
    )

    if symbol:
        query = query.filter(CryptoMetric.symbol == symbol.upper())

    crypto_data = query.order_by(
        CryptoMetric.date.asc(), CryptoMetric.market_cap_rank.asc()
    ).all()

    return [c.to_dict() for c in crypto_data]


@router.post("/crypto/collect")
async def collect_crypto_now(
    crypto_ids: Optional[List[str]] = Query(
        None, description="IDs de criptomonedas (bitcoin, ethereum, etc.)"
    ),
    db: Session = Depends(get_db),
):
    """Colecta datos de criptomonedas inmediatamente"""
    try:
        collector = CryptoCollector()
        cryptos = collector.collect_crypto(db, crypto_ids)
        return {
            "message": f"Collected data for {len(cryptos)} cryptocurrencies",
            "data": [c.to_dict() for c in cryptos],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error collecting crypto data: {str(e)}"
        )


# ==================== TFL ENDPOINTS ====================


@router.get("/tfl/latest")
async def get_latest_tfl(db: Session = Depends(get_db)):
    from sqlalchemy import func

    subquery = (
        db.query(TflMetric.line_id, func.max(TflMetric.date).label("max_date"))
        .group_by(TflMetric.line_id)
        .subquery()
    )

    # Obtener el registro completo de cada línea con su fecha más reciente
    tfl_data = (
        db.query(TflMetric)
        .join(
            subquery,
            and_(
                TflMetric.line_id == subquery.c.line_id,
                TflMetric.date == subquery.c.max_date,
            ),
        )
        .order_by(TflMetric.line_name.asc())
        .all()
    )

    if not tfl_data:
        raise HTTPException(status_code=404, detail="No TfL data found")

    return [t.to_dict() for t in tfl_data]


@router.get("/tfl/line/{line_id}")
async def get_tfl_line(line_id: str, db: Session = Depends(get_db)):
    """Obtiene el estado actual de una línea específica"""
    tfl = (
        db.query(TflMetric)
        .filter(TflMetric.line_id == line_id)
        .order_by(TflMetric.date.desc())
        .first()
    )

    if not tfl:
        raise HTTPException(status_code=404, detail=f"No data found for line {line_id}")

    return tfl.to_dict()


@router.get("/tfl/range")
async def get_tfl_range(
    start_date: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha final YYYY-MM-DD"),
    line_id: Optional[str] = Query(None, description="ID de línea específica"),
    db: Session = Depends(get_db),
):
    """Obtiene datos de TfL en un rango de fechas"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
        )

    if end < start:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    query = db.query(TflMetric).filter(
        and_(TflMetric.date >= start, TflMetric.date <= end)
    )

    if line_id:
        query = query.filter(TflMetric.line_id == line_id)

    tfl_data = query.order_by(TflMetric.date.asc()).all()

    return [t.to_dict() for t in tfl_data]


@router.post("/tfl/collect")
async def collect_tfl_now(db: Session = Depends(get_db)):
    """Colecta datos de TfL inmediatamente"""
    try:
        collector = TflCollector()
        tfl_data = collector.collect_line_status(db)
        return {
            "message": f"Collected status for {len(tfl_data)} TfL lines",
            "data": [t.to_dict() for t in tfl_data],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error collecting TfL data: {str(e)}"
        )


@router.get("/tfl/bikes")
async def get_bike_points():
    """Obtiene información actual de BikePoints (no se guarda en DB)"""
    try:
        collector = TflCollector()
        # No necesita db porque no guarda
        bike_data = collector.collect_bike_points(None, limit=50)
        return bike_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting bike points: {str(e)}"
        )


# ==================== STATS ENDPOINTS ====================


@router.get("/stats/summary")
async def get_summary_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas resumidas de todas las métricas"""
    weather_count = db.query(func.count(WeatherMetric.id)).scalar()
    crypto_count = db.query(func.count(CryptoMetric.id)).scalar()
    tfl_count = db.query(func.count(TflMetric.id)).scalar()  # CAMBIO AQUÍ

    latest_weather = db.query(WeatherMetric).order_by(WeatherMetric.date.desc()).first()
    latest_crypto = db.query(CryptoMetric).order_by(CryptoMetric.date.desc()).first()
    latest_tfl = (
        db.query(TflMetric).order_by(TflMetric.date.desc()).first()
    )  # CAMBIO AQUÍ

    return {
        "total_records": {
            "weather": weather_count,
            "crypto": crypto_count,
            "tfl": tfl_count,  # CAMBIO AQUÍ
        },
        "latest_dates": {
            "weather": latest_weather.date.isoformat() if latest_weather else None,
            "crypto": latest_crypto.date.isoformat() if latest_crypto else None,
            "tfl": latest_tfl.date.isoformat() if latest_tfl else None,  # CAMBIO AQUÍ
        },
    }
