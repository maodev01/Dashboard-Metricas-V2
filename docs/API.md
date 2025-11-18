# 📚 Documentación de API

API REST para el Dashboard de Métricas con actualización en tiempo real.

**Base URL**: `http://localhost:8000/api`

---

## 🔐 Autenticación

Actualmente la API es pública y no requiere autenticación.

---

## 📊 Endpoints

### Health Check

#### GET /health

Verifica el estado del servidor.

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Dashboard de Métricas",
  "version": "1.0.0"
}
```

---

## 🌤️ Weather Endpoints

### GET /api/weather/latest

Obtiene el registro más reciente del clima.

**Response:**
```json
{
  "id": 123,
  "date": "2025-11-04T15:30:00",
  "city": "Bucaramanga",
  "country": "CO",
  "temperature": 28.5,
  "feels_like": 30.2,
  "temp_min": 26.0,
  "temp_max": 31.0,
  "pressure": 1013,
  "humidity": 65,
  "weather_main": "Clouds",
  "weather_description": "nubes dispersas",
  "wind_speed": 3.5,
  "clouds": 40
}
```

### GET /api/weather/daily

Obtiene datos del clima para un día específico.

**Query Parameters:**
- `target_date` (optional): Fecha en formato YYYY-MM-DD

**Example:**
```bash
GET /api/weather/daily?target_date=2025-11-04
```

### GET /api/weather/range

Obtiene datos del clima en un rango de fechas.

**Query Parameters:**
- `start_date` (required): Fecha inicial YYYY-MM-DD
- `end_date` (required): Fecha final YYYY-MM-DD

**Example:**
```bash
GET /api/weather/range?start_date=2025-11-01&end_date=2025-11-04
```

**Response:**
```json
[
  {
    "id": 121,
    "date": "2025-11-01T12:00:00",
    "temperature": 27.5,
    ...
  },
  {
    "id": 122,
    "date": "2025-11-02T12:00:00",
    "temperature": 28.0,
    ...
  }
]
```

### POST /api/weather/collect

Colecta datos del clima inmediatamente.

**Query Parameters:**
- `city` (optional): Ciudad
- `country` (optional): País (código de 2 letras)

**Response:**
```json
{
  "message": "Weather data collected successfully",
  "data": { ... }
}
```

---

## 💰 Crypto Endpoints

### GET /api/crypto/latest

Obtiene los registros más recientes de criptomonedas.

**Response:**
```json
[
  {
    "id": 456,
    "date": "2025-11-04T15:32:00",
    "symbol": "BTC",
    "name": "Bitcoin",
    "current_price": 35000.50,
    "market_cap": 680000000000,
    "market_cap_rank": 1,
    "total_volume": 25000000000,
    "high_24h": 35500.00,
    "low_24h": 34500.00,
    "price_change_24h": 500.50,
    "price_change_percentage_24h": 1.45,
    "circulating_supply": 19500000,
    "total_supply": 21000000
  }
]
```

### GET /api/crypto/daily

Obtiene datos de criptomonedas para un día específico.

**Query Parameters:**
- `target_date` (optional): Fecha YYYY-MM-DD
- `symbol` (optional): Símbolo de crypto (BTC, ETH, etc.)

**Example:**
```bash
GET /api/crypto/daily?target_date=2025-11-04&symbol=BTC
```

### GET /api/crypto/range

Obtiene datos de criptomonedas en un rango de fechas.

**Query Parameters:**
- `start_date` (required): Fecha inicial
- `end_date` (required): Fecha final
- `symbol` (optional): Filtrar por símbolo

### POST /api/crypto/collect

Colecta datos de criptomonedas inmediatamente.

**Query Parameters:**
- `crypto_ids` (optional): Lista de IDs (bitcoin, ethereum, etc.)

---

## 🚇 TfL Endpoints

### GET /api/tfl/latest

Obtiene el estado más reciente de todas las líneas del metro de Londres.

**Response:**
```json
[
  {
    "id": 789,
    "date": "2025-11-04T15:34:00",
    "line_id": "victoria",
    "line_name": "Victoria",
    "status_severity": 10,
    "status_severity_description": "Good Service",
    "reason": null,
    "disruption_category": null,
    "closure_text": null
  },
  {
    "id": 790,
    "date": "2025-11-04T15:34:00",
    "line_id": "central",
    "line_name": "Central",
    "status_severity": 6,
    "status_severity_description": "Minor Delays",
    "reason": "Minor delays due to an earlier signal failure",
    "disruption_category": "Signal Problem",
    "closure_text": null
  }
]
```

**Status Severity Codes:**
- `10`: Good Service (Verde)
- `6-9`: Minor delays/issues (Amarillo)
- `0-5`: Severe delays/suspended (Rojo)

### GET /api/tfl/line/{line_id}

Obtiene el estado actual de una línea específica.

**Path Parameters:**
- `line_id`: ID de la línea (victoria, central, bakerloo, etc.)

**Example:**
```bash
GET /api/tfl/line/victoria
```

### GET /api/tfl/range

Obtiene datos históricos de TfL.

**Query Parameters:**
- `start_date` (required): Fecha inicial
- `end_date` (required): Fecha final
- `line_id` (optional): Filtrar por línea

### GET /api/tfl/bikes

Obtiene información actual de BikePoints (puntos de bicicletas públicas).

**Response:**
```json
{
  "total_points": 778,
  "sample_size": 50,
  "bike_points": [
    {
      "id": "BikePoints_1",
      "commonName": "River Street, Clerkenwell",
      "lat": 51.5292,
      "lon": -0.1089,
      "bikes_available": 12,
      "empty_docks": 7,
      "total_docks": 19
    }
  ]
}
```

### POST /api/tfl/collect

Colecta datos de TfL inmediatamente.

**Response:**
```json
{
  "message": "Collected status for 11 TfL lines",
  "data": [ ... ]
}
```

---

## 📈 Stats Endpoints

### GET /api/stats/summary

Obtiene estadísticas resumidas de todas las métricas.

**Response:**
```json
{
  "total_records": {
    "weather": 1250,
    "crypto": 3840,
    "tfl": 5520
  },
  "latest_dates": {
    "weather": "2025-11-04T15:30:00",
    "crypto": "2025-11-04T15:32:00",
    "tfl": "2025-11-04T15:34:00"
  }
}
```

---

## ⚡ Actualización Automática

El sistema colecta datos automáticamente cada **2 minutos** para:
- Clima (OpenWeatherMap)
- Criptomonedas (CoinGecko)
- TfL Transport (Transport for London)

Los datos se almacenan en PostgreSQL con timestamp para análisis histórico.

---

## 🔧 Rate Limiting

**Límites actuales:**
- Sin límites implementados en la API
- Respeta límites de APIs externas:
  - OpenWeatherMap: 1,000 calls/day
  - CoinGecko: Sin límite oficial
  - TfL: Sin límite oficial

---

## ❌ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | Success |
| 400 | Bad Request (formato inválido) |
| 404 | Not Found (sin datos) |
| 500 | Internal Server Error |

**Formato de Error:**
```json
{
  "detail": "Mensaje de error descriptivo"
}
```

---

## 📝 Notas

- Todos los timestamps están en UTC
- Los datos se actualizan cada 2 minutos automáticamente
- El frontend tiene auto-refresh sincronizado
- Para documentación interactiva: http://localhost:8000/docs

---

**Última actualización**: 2025-11-04