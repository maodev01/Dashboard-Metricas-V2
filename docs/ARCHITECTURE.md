# Arquitectura del Sistema - Dashboard de Métricas

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO FINAL                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/HTTPS
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                      NGINX (Reverse Proxy)                       │
│  - Servidor estático (Frontend)                                  │
│  - Proxy a Backend API                                          │
│  - SSL/TLS Termination                                          │
└────────────┬────────────────────────────────┬────────────────────┘
             │                                 │
             │ Static Files                    │ /api/*
             ↓                                 ↓
┌──────────────────────┐          ┌──────────────────────────────┐
│   FRONTEND           │          │   BACKEND (FastAPI)          │
│  ─────────────       │          │  ─────────────────────       │
│  • HTML5             │          │  • FastAPI Framework         │
│  • Chart.js          │          │  • SQLAlchemy ORM            │
│  • Tailwind CSS      │          │  • APScheduler               │
│  • Vanilla JS        │          │  • Pydantic                  │
└──────────────────────┘          └────────┬────────────┬────────┘
                                           │            │
                        ┌──────────────────┘            │
                        │                               │
                        ↓                               ↓
            ┌──────────────────────┐      ┌────────────────────┐
            │   PostgreSQL DB      │      │   COLLECTORS       │
            │  ───────────────     │      │  ───────────       │
            │  • weather_metrics   │      │  • WeatherAPI      │
            │  • crypto_metrics    │      │  • CoinGecko       │
            │  • nasa_metrics      │      │  • TLF Transport   │
            └──────────────────────┘      └────────────────────┘
                                                    │
                                                    ↓
                                          ┌──────────────────┐
                                          │  EXTERNAL APIs   │
                                          │  ─────────────   │
                                          │  • OpenWeather   │
                                          │  • CoinGecko     │
                                          │  • NASA          │
                                          └──────────────────┘
```

---

## 🏗️ Componentes del Sistema

### 1. Frontend (Capa de Presentación)

**Tecnologías**: HTML5, CSS3 (Tailwind), JavaScript (ES6+), Chart.js

**Responsabilidades**:
- Renderizar interfaz de usuario
- Visualizar datos en gráficos interactivos
- Manejar interacciones del usuario
- Comunicarse con el backend vía REST API

**Archivos principales**:
```
frontend/
├── index.html           # Página principal
├── js/
│   ├── config.js       # Configuración
│   ├── api.js          # Cliente API
│   ├── charts.js       # Gráficos
│   └── dashboard.js    # Lógica principal
```

**Flujo de datos**:
1. Usuario accede a la página
2. JavaScript carga automáticamente datos del backend
3. Datos se procesan y visualizan en charts
4. Usuario puede filtrar por rango de fechas
5. Actualización bajo demanda con botones

---

### 2. Backend (Capa de Lógica de Negocio)

**Tecnologías**: Python 3.11+, FastAPI, SQLAlchemy, APScheduler

**Responsabilidades**:
- Exponer API REST
- Colectar datos de APIs externas
- Almacenar datos en base de datos
- Programar tareas automáticas
- Validar y transformar datos

**Estructura**:
```
backend/
├── main.py              # App principal
├── config.py            # Configuración
├── database.py          # Setup DB
├── models.py            # Modelos SQLAlchemy
├── routes.py            # Endpoints API
├── scheduler.py         # Tareas programadas
└── collectors/
    ├── weather.py       # Colector clima
    ├── crypto.py        # Colector cripto
    └── tfl.py           # Colector TFL
```

**Patrones de diseño**:
- **Repository Pattern**: Abstracción de acceso a datos
- **Dependency Injection**: FastAPI Depends para DB sessions
- **Singleton**: Scheduler único
- **Strategy Pattern**: Diferentes colectores con interfaz común

---

### 3. Base de Datos (Capa de Persistencia)

**Tecnología**: PostgreSQL 15 (SQLite para desarrollo)

**Esquema**:

```sql
-- Tabla de métricas del clima
CREATE TABLE weather_metrics (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    city VARCHAR(100),
    country VARCHAR(10),
    temperature FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    pressure INTEGER,
    humidity INTEGER,
    weather_main VARCHAR(50),
    weather_description VARCHAR(200),
    wind_speed FLOAT,
    clouds INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_weather_date ON weather_metrics(date);

-- Tabla de métricas de criptomonedas
CREATE TABLE crypto_metrics (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(100),
    current_price FLOAT,
    market_cap FLOAT,
    market_cap_rank INTEGER,
    total_volume FLOAT,
    high_24h FLOAT,
    low_24h FLOAT,
    price_change_24h FLOAT,
    price_change_percentage_24h FLOAT,
    circulating_supply FLOAT,
    total_supply FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_crypto_date ON crypto_metrics(date);
CREATE INDEX idx_crypto_symbol ON crypto_metrics(symbol);

-- Tabla de métricas de NASA
CREATE TABLE nasa_metrics (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    apod_date VARCHAR(10) NOT NULL,
    title VARCHAR(500),
    explanation TEXT,
    url VARCHAR(1000),
    hdurl VARCHAR(1000),
    media_type VARCHAR(50),
    copyright VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_nasa_apod_date ON nasa_metrics(apod_date);
```

---

### 4. Scheduler (Automatización)

**Tecnología**: APScheduler

**Funcionamiento**:
```python
# Configurado en scheduler.py
scheduler.add_job(
    func=collect_all_metrics,
    trigger=CronTrigger(hour=0, minute=0),  # Medianoche UTC
    id='daily_metrics_collection'
)
```

**Tareas programadas**:
- Colección diaria de datos del clima
- Colección diaria de precios de criptomonedas
- Colección diaria de NASA APOD

---

### 5. Collectors (Integraciones Externas)

**APIs Integradas**:

#### OpenWeatherMap API
- **Endpoint**: `https://api.openweathermap.org/data/2.5/weather`
- **Frecuencia**: 1x por día
- **Datos**: Temperatura, humedad, presión, viento, nubes

#### CoinGecko API
- **Endpoint**: `https://api.coingecko.com/api/v3/coins/markets`
- **Frecuencia**: 1x por día
- **Datos**: Precios, market cap, volumen, cambios 24h

#### TFL TRANSPORT API
- **Endpoint**: `https://api.tfl.gov.uk/`
- **Frecuencia**: Hasta 50x por día
- **Datos**: Flujo de Trafico, Colas

---

## 🔄 Flujos de Datos

### Flujo de Colección Automática

```
1. APScheduler trigger (medianoche UTC)
   ↓
2. scheduler.collect_all_metrics()
   ↓
3. Para cada collector:
   ├─→ weather_collector.collect_weather()
   │   ├─→ GET OpenWeatherMap API
   │   ├─→ Parse JSON response
   │   └─→ INSERT into weather_metrics
   │
   ├─→ crypto_collector.collect_crypto()
   │   ├─→ GET CoinGecko API
   │   ├─→ Parse JSON response
   │   └─→ INSERT into crypto_metrics
   │
   └─→ tfl_collector.collect_tfl()
       ├─→ GET TLF TRANSPORT API
       ├─→ Parse JSON response
       └─→ INSERT into tfl_metrics
   ↓
4. Log de resultados
```

### Flujo de Consulta de Datos

```
1. Usuario abre frontend
   ↓
2. JavaScript ejecuta API calls
   ├─→ GET /api/weather/latest
   ├─→ GET /api/crypto/latest
   ├─→ GET /api/tfl/latest
   └─→ GET /api/stats/summary
   ↓
3. Backend procesa requests
   ├─→ Query a PostgreSQL
   ├─→ Transform con SQLAlchemy
   └─→ Serialize con Pydantic
   ↓
4. Response JSON al frontend
   ↓
5. Frontend renderiza:
   ├─→ Actualiza cards
   ├─→ Genera gráficos Chart.js
   └─→ Muestra Grafico TFL Transport
```

### Flujo de Colección Manual

```
1. Usuario click "Colectar Datos"
   ↓
2. POST /api/weather/collect
   POST /api/crypto/collect
   POST /api/tfl/collect
   ↓
3. Collectors ejecutan inmediatamente
   ↓
4. Datos guardados en DB
   ↓
5. Response 200 OK
   ↓
6. Frontend muestra notificación
   ↓
7. Auto-refresh de datos
```

---

## 🔐 Seguridad

### Autenticación y Autorización
- **Actual**: Sin autenticación (API pública)
- **Recomendado para producción**:
  - JWT tokens
  - API keys por usuario
  - OAuth2 con FastAPI

### Validación de Datos
- Pydantic schemas en todos los endpoints
- Validación de tipos y rangos
- Sanitización de inputs

### CORS
- Configurado en backend para permitir frontend
- Restringir origins en producción

### Variables de Entorno
- API keys en `.env` (nunca en código)
- Secrets en CI/CD con GitHub Secrets

### Rate Limiting
- **Recomendado**: Implementar con slowapi
- Límites por IP y por endpoint

---

## 📈 Escalabilidad

### Estrategias de Escalado

#### Horizontal (Múltiples instancias)
```yaml
# docker-compose scale
docker-compose up -d --scale backend=3
```
Requiere:
- Load balancer (Nginx/HAProxy)
- Redis para sesiones compartidas
- PostgreSQL externo

#### Vertical (Más recursos)
- Aumentar CPU/RAM del servidor
- Optimizar queries de DB
- Índices en campos frecuentes

### Caching
Implementar Redis para:
- Caché de queries frecuentes
- Resultados de APIs externas (1 hora)
- Rate limiting distribuido

### Queue System
Para colecciones pesadas:
- Celery + Redis
- RabbitMQ
- AWS SQS

---

## 🧪 Testing

### Niveles de Testing

#### Unit Tests
```python
# test_models.py
def test_weather_model():
    weather = WeatherMetric(temperature=25.0)
    assert weather.temperature == 25.0
```

#### Integration Tests
```python
# test_api.py
def test_get_weather_endpoint():
    response = client.get("/api/weather/latest")
    assert response.status_code == 200
```

#### E2E Tests
- Selenium para frontend
- Pruebas de flujos completos

### Coverage
```bash
pytest --cov=. --cov-report=html
# Target: >80% coverage
```

---

## 📊 Monitoreo

### Métricas a Monitorear

#### Sistema
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

#### Aplicación
- Request rate (req/s)
- Response time (p50, p95, p99)
- Error rate (%)
- Success rate (%)

#### Base de Datos
- Query time
- Connection pool
- Locks
- Index usage

### Herramientas Recomendadas

- **Prometheus**: Métricas
- **Grafana**: Visualización
- **Loki**: Logs agregados
- **Sentry**: Error tracking

---

## 🔄 CI/CD Pipeline

### Stages

1. **Lint**: Verificar código con flake8, black
2. **Test**: Ejecutar pytest con coverage
3. **Build**: Construir imágenes Docker
4. **Security**: Scan con Trivy
5. **Deploy**: Desplegar a producción
6. **Smoke Test**: Verificar servicios funcionando

### Environments

- **Development**: Auto-deploy en cada push
- **Staging**: Deploy manual o con tag
- **Production**: Deploy manual + aprobación

---

## 📦 Dependencias

### Backend
```
fastapi==0.104.1        # Framework web
uvicorn==0.24.0         # ASGI server
sqlalchemy==2.0.23      # ORM
requests==2.31.0        # HTTP client
APScheduler==3.10.4     # Scheduler
psycopg2-binary==2.9.9  # PostgreSQL driver
```

### Frontend
```
Chart.js 4.4.0          # Gráficos
Tailwind CSS 3.x        # Estilos
Font Awesome 6.4        # Iconos
```

## ⚡ Sistema de Actualización en Tiempo Real

### Backend: Scheduler cada 2 minutos
```python
# scheduler.py
trigger = IntervalTrigger(minutes=2)
scheduler.add_job(collect_all_metrics, trigger=trigger)
```

**Flujo:**
```
Cada 2 minutos:
  1. APScheduler trigger
  2. collect_all_metrics()
  3. weather_collector.collect()
  4. crypto_collector.collect()
  5. tfl_collector.collect()
  6. Guardar en PostgreSQL
  7. Log de resultados
```

### Frontend: Auto-Refresh
```javascript
// dashboard.js
setInterval(refreshAllData, 120000); // 2 minutos
```

**Flujo:**
```
Cada 2 minutos:
  1. Timer ejecuta refreshAllData()
  2. Fetch APIs:
     - /api/weather/latest
     - /api/crypto/latest
     - /api/tfl/latest
  3. Actualizar gráficos
  4. Actualizar cards
  5. Mostrar timestamp
```

### Sincronización

- **Backend**: Colecta datos cada 2 min
- **Frontend**: Actualiza UI cada 2 min
- **Offset**: Frontend espera 10s después del backend

Esto asegura que el frontend siempre muestre los datos más recientes.

---

## 🚀 Roadmap Futuro

### Features Planificados

- [ ] Autenticación de usuarios
- [ ] Dashboard personalizable
- [ ] Exportar datos a CSV/PDF
- [ ] Alertas por email/SMS
- [ ] Más fuentes de datos
- [ ] Modo oscuro
- [ ] PWA (Progressive Web App)
- [ ] WebSockets para real-time
- [ ] Machine Learning predictions
- [ ] API GraphQL

---

## 📚 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Chart.js Docs](https://www.chartjs.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Docs](https://docs.docker.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Versión**: 1.0.0  
**Última actualización**: Octubre 2024