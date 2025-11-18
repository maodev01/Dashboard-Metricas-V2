from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app
from backend.models import CryptoMetric, WeatherMetric, TflMetric

# --- Configuración Base de Datos Test ---
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- Fixtures ---


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_weather_data(db_session):
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
def sample_tfl_data(db_session):
    """Crea datos de prueba de TFL"""
    tfl = TflMetric(
        date=datetime.utcnow(),
        line_name="Central",
        status_description="Good Service",
        reason=None,
    )
    db_session.add(tfl)
    db_session.commit()
    db_session.refresh(tfl)
    return tfl


# --- Tests generales ---


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# --- WEATHER ---


def test_get_latest_weather_empty():
    response = client.get("/api/weather/latest")
    assert response.status_code == 404


def test_get_latest_weather(sample_weather_data):
    response = client.get("/api/weather/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Test City"


def test_get_weather_range(sample_weather_data):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    response = client.get(
        f"/api/weather/range?start_date={yesterday}&end_date={tomorrow}"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_weather_range_invalid_dates():
    response = client.get("/api/weather/range?start_date=xxx&end_date=xxx")
    assert response.status_code == 400


# --- CRYPTO ---


def test_get_latest_crypto_empty():
    response = client.get("/api/crypto/latest")
    assert response.status_code == 404


def test_get_latest_crypto(sample_crypto_data):
    response = client.get("/api/crypto/latest")
    data = response.json()
    assert len(data) > 0
    assert data[0]["symbol"] == "BTC"


def test_get_crypto_range(sample_crypto_data):
    today = datetime.now().date()
    response = client.get(
        f"/api/crypto/range?start_date={today}&end_date={today}"
    )
    assert response.status_code == 200


def test_get_crypto_by_symbol(sample_crypto_data):
    today = datetime.now().date()
    response = client.get(f"/api/crypto/daily?target_date={today}&symbol=BTC")
    assert response.status_code == 200


# --- TFL ---


def test_get_latest_tfl_empty():
    response = client.get("/api/tfl/latest")
    assert response.status_code == 404


def test_get_latest_tfl(sample_tfl_data):
    response = client.get("/api/tfl/latest")
    data = response.json()
    assert data["line_name"] == "Central"
    assert data["status_description"] == "Good Service"


def test_get_tfl_range(sample_tfl_data):
    today = datetime.now().date()
    response = client.get(
        f"/api/tfl/range?start_date={today}&end_date={today}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --- Stats ---


def test_get_stats_summary(sample_weather_data, sample_crypto_data, sample_tfl_data):
    response = client.get("/api/stats/summary")
    assert response.status_code == 200
    data = response.json()

    assert "total_records" in data
    assert "latest_dates" in data

    assert data["total_records"]["weather"] >= 1
    assert data["total_records"]["crypto"] >= 1
    assert data["total_records"]["tfl"] >= 1


# --- Modelos ---


def test_weather_model_to_dict(sample_weather_data):
    assert isinstance(sample_weather_data.to_dict(), dict)


def test_crypto_model_to_dict(sample_crypto_data):
    assert sample_crypto_data.to_dict()["symbol"] == "BTC"


def test_tfl_model_to_dict(sample_tfl_data):
    assert sample_tfl_data.to_dict()["line_name"] == "Central"


# --- Cleanup ---


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)
