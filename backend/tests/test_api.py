from datetime import datetime
from datetime import timedelta

import pytest
from database import Base
from database import get_db
from fastapi.testclient import TestClient
from main import app
from models import CryptoMetric
from models import NasaMetric
from models import WeatherMetric
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurar base de datos de prueba
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Override de la dependencia de DB


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Cliente de pruebas
client = TestClient(app)

# Fixtures


@pytest.fixture
def db_session():
    """Proporciona una sesión de base de datos para pruebas"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_weather_data(db_session):
    """Crea datos de prueba de clima"""
    weather = WeatherMetric(
        date=datetime.utcnow(),
        city="Test City",
        country="TC",
        temperature=25.0,
        feels_like=24.0,
        temp_min=20.0,
        temp_max=30.0,
        pressure=1013,
        humidity=60,
        weather_main="Clear",
        weather_description="clear sky",
        wind_speed=5.0,
        clouds=10,
    )
    db_session.add(weather)
    db_session.commit()
    db_session.refresh(weather)
    return weather


@pytest.fixture
def sample_crypto_data(db_session):
    """Crea datos de prueba de criptomonedas"""
    crypto = CryptoMetric(
        date=datetime.utcnow(),
        symbol="BTC",
        name="Bitcoin",
        current_price=50000.0,
        market_cap=1000000000000,
        market_cap_rank=1,
        total_volume=50000000000,
        high_24h=51000.0,
        low_24h=49000.0,
        price_change_24h=1000.0,
        price_change_percentage_24h=2.0,
        circulating_supply=19000000,
        total_supply=21000000,
    )
    db_session.add(crypto)
    db_session.commit()
    db_session.refresh(crypto)
    return crypto


@pytest.fixture
def sample_nasa_data(db_session):
    """Crea datos de prueba de NASA"""
    nasa = NasaMetric(
        date=datetime.utcnow(),
        apod_date="2024-01-01",
        title="Test APOD",
        explanation="This is a test explanation",
        url="https://example.com/image.jpg",
        hdurl="https://example.com/image_hd.jpg",
        media_type="image",
        copyright="Test Copyright",
    )
    db_session.add(nasa)
    db_session.commit()
    db_session.refresh(nasa)
    return nasa


# ==================== TESTS DE ENDPOINTS PRINCIPALES ====================


def test_root_endpoint():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health_check():
    """Test del health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# ==================== TESTS DE WEATHER ====================


def test_get_latest_weather_empty():
    """Test obtener clima sin datos"""
    response = client.get("/api/weather/latest")
    assert response.status_code == 404


def test_get_latest_weather(sample_weather_data):
    """Test obtener último registro de clima"""
    response = client.get("/api/weather/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Test City"
    assert data["temperature"] == 25.0


def test_get_weather_range(sample_weather_data):
    """Test obtener clima en rango de fechas"""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    response = client.get(
        f"/api/weather/range?start_date={yesterday}&end_date={tomorrow}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_weather_range_invalid_dates():
    """Test con fechas inválidas"""
    response = client.get("/api/weather/range?start_date=invalid&end_date=invalid")
    assert response.status_code == 400


# ==================== TESTS DE CRYPTO ====================


def test_get_latest_crypto_empty():
    """Test obtener crypto sin datos"""
    response = client.get("/api/crypto/latest")
    assert response.status_code == 404


def test_get_latest_crypto(sample_crypto_data):
    """Test obtener últimos registros de crypto"""
    response = client.get("/api/crypto/latest")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["symbol"] == "BTC"


def test_get_crypto_range(sample_crypto_data):
    """Test obtener crypto en rango de fechas"""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    response = client.get(
        f"/api/crypto/range?start_date={yesterday}&end_date={tomorrow}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_crypto_by_symbol(sample_crypto_data):
    """Test filtrar crypto por símbolo"""
    today = datetime.now().date()
    response = client.get(f"/api/crypto/daily?target_date={today}&symbol=BTC")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert data[0]["symbol"] == "BTC"


# ==================== TESTS DE NASA ====================


def test_get_latest_nasa_empty():
    """Test obtener NASA sin datos"""
    response = client.get("/api/nasa/latest")
    assert response.status_code == 404


def test_get_latest_nasa(sample_nasa_data):
    """Test obtener último APOD"""
    response = client.get("/api/nasa/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test APOD"
    assert data["media_type"] == "image"


def test_get_nasa_range(sample_nasa_data):
    """Test obtener NASA en rango de fechas"""
    response = client.get("/api/nasa/range?start_date=2024-01-01&end_date=2024-01-02")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# ==================== TESTS DE STATS ====================


def test_get_stats_summary(sample_weather_data, sample_crypto_data, sample_nasa_data):
    """Test obtener resumen de estadísticas"""
    response = client.get("/api/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "latest_dates" in data
    assert data["total_records"]["weather"] >= 1
    assert data["total_records"]["crypto"] >= 1
    assert data["total_records"]["nasa"] >= 1


# ==================== TESTS DE MODELOS ====================


def test_weather_model_to_dict(sample_weather_data):
    """Test del método to_dict del modelo Weather"""
    data = sample_weather_data.to_dict()
    assert isinstance(data, dict)
    assert "id" in data
    assert "temperature" in data
    assert data["city"] == "Test City"


def test_crypto_model_to_dict(sample_crypto_data):
    """Test del método to_dict del modelo Crypto"""
    data = sample_crypto_data.to_dict()
    assert isinstance(data, dict)
    assert "symbol" in data
    assert data["symbol"] == "BTC"
    assert "current_price" in data


def test_nasa_model_to_dict(sample_nasa_data):
    """Test del método to_dict del modelo NASA"""
    data = sample_nasa_data.to_dict()
    assert isinstance(data, dict)
    assert "title" in data
    assert data["title"] == "Test APOD"


# ==================== CLEANUP ====================


def teardown_module(module):
    """Limpiar después de todos los tests"""
    Base.metadata.drop_all(bind=engine)
