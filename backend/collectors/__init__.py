# backend/collectors/__init__.py

from .crypto import CryptoCollector
from .tfl import TflCollector
from .weather import WeatherCollector

__all__ = ["WeatherCollector", "CryptoCollector", "TflCollector"]
