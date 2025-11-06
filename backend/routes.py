from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import datetime, date, timedelta
from database import get_db
from models import WeatherMetric, CryptoMetric, NasaMetric
from collectors.weather import WeatherCollector
from collectors.crypto import CryptoCollector
from collectors.nasa import NasaCollector
import logging

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
    db: Session = Depends(get_db)
):
    """Obtiene datos del clima para un día específico"""
    if target_date:
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        parsed_date = date.today()
    
    # Buscar registros del día específico
    weather = db.query(WeatherMetric).filter(
        func.date(WeatherMetric.date) == parsed_date
    ).order_by(WeatherMetric.date.desc()).first()
    
    if not weather:
        raise HTTPException(status_code=404, detail=f"No weather data found for {parsed_date}")
    
    return weather.to_dict()

@router.get("/weather/range")
async def get_weather_range(
    start_date: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha final YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Obtiene datos del clima en un rango de fechas"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if end < start:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")
    
    weather_data = db.query(WeatherMetric).filter(
        and_(
            WeatherMetric.date >= start,
            WeatherMetric.date <= end
        )
    ).order_by(WeatherMetric.date.asc()).all()
    
    return [w.to_dict() for w in weather_data]

@router.post("/weather/collect")
async def collect_weather_now(
    city: Optional[str] = None,
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Colecta datos del clima inmediatamente"""
    try:
        collector = WeatherCollector()
        weather = collector.collect_weather(db, city, country)
        return {
            "message": "Weather data collected successfully",
            "data": weather.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error collecting weather data: {str(e)}")

# ==================== CRYPTO ENDPOINTS ====================

@router.get("/crypto/latest")
async def get_latest_crypto(db: Session = Depends(get_db)):
    """Obtiene los registros más recientes de criptomonedas"""
    # Obtener la fecha más reciente
    latest_date = db.query(func.max(CryptoMetric.date)).scalar()
    if not latest_date:
        raise HTTPException(status_code=404, detail="No crypto data found")
    
    cryptos = db.query(CryptoMetric).filter(
        func.date(CryptoMetric.date) == latest_date.date()
    ).order_by(CryptoMetric.market_cap_rank.asc()).all()
    
    return [c.to_dict() for c in cryptos]

@router.get("/crypto/daily")
async def get_daily_crypto(
    target_date: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    symbol: Optional[str] = Query(None, description="Símbolo de la criptomoneda (BTC, ETH, etc.)"),
    db: Session = Depends(get_db)
):
    """Obtiene datos de criptomonedas para un día específico"""
    if target_date:
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        parsed_date = date.today()
    
    query = db.query(CryptoMetric).filter(func.date(CryptoMetric.date) == parsed_date)
    
    if symbol:
        query = query.filter(CryptoMetric.symbol == symbol.upper())
    
    cryptos = query.order_by(CryptoMetric.market_cap_rank.asc()).all()
    
    if not cryptos:
        raise HTTPException(status_code=404, detail=f"No crypto data found for {parsed_date}")
    
    return [c.to_dict() for c in cryptos]

@router.get("/crypto/range")
async def get_crypto_range(
    start_date: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha final YYYY-MM-DD"),
    symbol: Optional[str] = Query(None, description="Símbolo de la criptomoneda"),
    db: Session = Depends(get_db)
):
    """Obtiene datos de criptomonedas en un rango de fechas"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if end < start:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")
    
    query = db.query(CryptoMetric).filter(
        and_(
            CryptoMetric.date >= start,
            CryptoMetric.date <= end
        )
    )
    
    if symbol:
        query = query.filter(CryptoMetric.symbol == symbol.upper())
    
    crypto_data = query.order_by(CryptoMetric.date.asc(), CryptoMetric.market_cap_rank.asc()).all()
    
    return [c.to_dict() for c in crypto_data]

@router.post("/crypto/collect")
async def collect_crypto_now(
    crypto_ids: Optional[List[str]] = Query(None, description="IDs de criptomonedas (bitcoin, ethereum, etc.)"),
    db: Session = Depends(get_db)
):
    """Colecta datos de criptomonedas inmediatamente"""
    try:
        collector = CryptoCollector()
        cryptos = collector.collect_crypto(db, crypto_ids)
        return {
            "message": f"Collected data for {len(cryptos)} cryptocurrencies",
            "data": [c.to_dict() for c in cryptos]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error collecting crypto data: {str(e)}")

# ==================== NASA ENDPOINTS ====================

@router.get("/nasa/latest")
async def get_latest_nasa(db: Session = Depends(get_db)):
    """Obtiene el registro más reciente de NASA APOD"""
    nasa = db.query(NasaMetric).order_by(NasaMetric.date.desc()).first()
    if not nasa:
        raise HTTPException(status_code=404, detail="No NASA data found")
    return nasa.to_dict()

@router.get("/nasa/daily")
async def get_daily_nasa(
    target_date: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Obtiene NASA APOD para un día específico"""
    if target_date:
        apod_date = target_date
    else:
        apod_date = str(date.today())
    
    nasa = db.query(NasaMetric).filter(
        NasaMetric.apod_date == apod_date
    ).order_by(NasaMetric.date.desc()).first()
    
    if not nasa:
        raise HTTPException(status_code=404, detail=f"No NASA APOD data found for {apod_date}")
    
    return nasa.to_dict()

@router.get("/nasa/range")
async def get_nasa_range(
    start_date: str = Query(..., description="Fecha inicial YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha final YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Obtiene NASA APOD en un rango de fechas"""
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    nasa_data = db.query(NasaMetric).filter(
        and_(
            NasaMetric.apod_date >= start_date,
            NasaMetric.apod_date <= end_date
        )
    ).order_by(NasaMetric.apod_date.asc()).all()
    
    return [n.to_dict() for n in nasa_data]

@router.post("/nasa/collect")
async def collect_nasa_now(
    apod_date: Optional[str] = Query(None, description="Fecha YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Colecta datos de NASA APOD inmediatamente"""
    try:
        collector = NasaCollector()
        nasa = collector.collect_apod(db, apod_date)
        return {
            "message": "NASA APOD data collected successfully",
            "data": nasa.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error collecting NASA data: {str(e)}")

# ==================== STATS ENDPOINTS ====================

@router.get("/stats/summary")
async def get_summary_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas resumidas de todas las métricas"""
    weather_count = db.query(func.count(WeatherMetric.id)).scalar()
    crypto_count = db.query(func.count(CryptoMetric.id)).scalar()
    nasa_count = db.query(func.count(NasaMetric.id)).scalar()
    
    latest_weather = db.query(WeatherMetric).order_by(WeatherMetric.date.desc()).first()
    latest_crypto = db.query(CryptoMetric).order_by(CryptoMetric.date.desc()).first()
    latest_nasa = db.query(NasaMetric).order_by(NasaMetric.date.desc()).first()
    
    return {
        "total_records": {
            "weather": weather_count,
            "crypto": crypto_count,
            "nasa": nasa_count
        },
        "latest_dates": {
            "weather": latest_weather.date.isoformat() if latest_weather else None,
            "crypto": latest_crypto.date.isoformat() if latest_crypto else None,
            "nasa": latest_nasa.date.isoformat() if latest_nasa else None
        }
    }