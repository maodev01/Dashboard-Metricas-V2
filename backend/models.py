from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from backend.database import Base


class WeatherMetric(Base):
    __tablename__ = "weather_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    city = Column(String(100))
    country = Column(String(10))
    temperature = Column(Float)  # Celsius
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)  # hPa
    humidity = Column(Integer)  # %
    weather_main = Column(String(50))
    weather_description = Column(String(200))
    wind_speed = Column(Float)  # m/s
    clouds = Column(Integer)  # %
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "city": self.city,
            "country": self.country,
            "temperature": self.temperature,
            "feels_like": self.feels_like,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "pressure": self.pressure,
            "humidity": self.humidity,
            "weather_main": self.weather_main,
            "weather_description": self.weather_description,
            "wind_speed": self.wind_speed,
            "clouds": self.clouds,
        }


class CryptoMetric(Base):
    __tablename__ = "crypto_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    symbol = Column(String(10), index=True)  # BTC, ETH, etc.
    name = Column(String(100))
    current_price = Column(Float)
    market_cap = Column(Float)
    market_cap_rank = Column(Integer)
    total_volume = Column(Float)
    high_24h = Column(Float)
    low_24h = Column(Float)
    price_change_24h = Column(Float)
    price_change_percentage_24h = Column(Float)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "symbol": self.symbol,
            "name": self.name,
            "current_price": self.current_price,
            "market_cap": self.market_cap,
            "market_cap_rank": self.market_cap_rank,
            "total_volume": self.total_volume,
            "high_24h": self.high_24h,
            "low_24h": self.low_24h,
            "price_change_24h": self.price_change_24h,
            "price_change_percentage_24h": self.price_change_percentage_24h,
            "circulating_supply": self.circulating_supply,
            "total_supply": self.total_supply,
        }


class TflMetric(Base):
    __tablename__ = "tfl_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    line_id = Column(String(50), index=True)  # ej: "victoria", "central"
    line_name = Column(String(100))
    status_severity = Column(Integer)  # 0-20 (10=Good Service)
    status_severity_description = Column(String(50))  # "Good Service", "Minor Delays"
    reason = Column(Text, nullable=True)  # Razón del estado
    disruption_category = Column(String(100), nullable=True)
    closure_text = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "line_id": self.line_id,
            "line_name": self.line_name,
            "status_severity": self.status_severity,
            "status_severity_description": self.status_severity_description,
            "reason": self.reason,
            "disruption_category": self.disruption_category,
            "closure_text": self.closure_text,
        }
