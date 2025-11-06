from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

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
            "clouds": self.clouds
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
            "total_supply": self.total_supply
        }


class NasaMetric(Base):
    __tablename__ = "nasa_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    apod_date = Column(String(10))  # Fecha del APOD (YYYY-MM-DD)
    title = Column(String(500))
    explanation = Column(Text)
    url = Column(String(1000))
    hdurl = Column(String(1000), nullable=True)
    media_type = Column(String(50))
    copyright = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "apod_date": self.apod_date,
            "title": self.title,
            "explanation": self.explanation,
            "url": self.url,
            "hdurl": self.hdurl,
            "media_type": self.media_type,
            "copyright": self.copyright
        }