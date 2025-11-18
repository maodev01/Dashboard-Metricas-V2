# Backend - Dashboard de Métricas

Backend completo con FastAPI para colectar y servir métricas de clima, criptomonedas y NASA APOD.

## 📁 Estructura del Proyecto

```
backend/
├── collectors/
│   ├── __init__.py
│   ├── weather.py       # Colector de datos del clima
│   ├── crypto.py        # Colector de criptomonedas
│   └── nasa.py          # Colector de NASA APOD
├── config.py            # Configuración de la aplicación
├── database.py          # Configuración de la base de datos
├── models.py            # Modelos de SQLAlchemy
├── routes.py            # Endpoints de la API
├── scheduler.py         # Scheduler para colección automática
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── Dockerfile          # Imagen Docker
└── .env.example        # Ejemplo de variables de entorno
```

## 🚀 Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` y agregar tus API keys:

- **OpenWeatherMap**: Obtener gratis en https://openweathermap.org/api
- **NASA**: Obtener gratis en https://api.nasa.gov/ (o usar DEMO_KEY)
- **CoinGecko**: No requiere API key

### 4. Ejecutar la aplicación

```bash
# Modo desarrollo con auto-reload
uvicorn main:app --reload

# O usando Python directamente
python main.py
```

La API estará disponible en: http://localhost:8000

## 📚 Documentación de la API

Una vez ejecutando, visita:

- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## 🔌 Endpoints Principales

### Weather (Clima)

```
GET  /api/weather/latest                    # Último registro
GET  /api/weather/daily?target_date=YYYY-MM-DD  # Datos de un día
GET  /api/weather/range?start_date=...&end_date=...  # Rango de fechas
POST /api/weather/collect                   # Colectar ahora
```

### Crypto (Criptomonedas)

```
GET  /api/crypto/latest                     # Últimos registros
GET  /api/crypto/daily?target_date=YYYY-MM-DD&symbol=BTC  # Datos de un día
GET  /api/crypto/range?start_date=...&end_date=...&symbol=BTC  # Rango
POST /api/crypto/collect                    # Colectar ahora
```

### NASA

```
GET  /api/nasa/latest                       # Último APOD
GET  /api/nasa/daily?target_date=YYYY-MM-DD # APOD de un día
GET  /api/nasa/range?start_date=...&end_date=...  # Rango de APODs
POST /api/nasa/collect                      # Colectar ahora
```

### Estadísticas

```
GET  /api/stats/summary                     # Resumen de todas las métricas
```

## 🕐 Colección Automática

El sistema incluye un scheduler que automáticamente colecta todas las métricas diariamente a la hora configurada en `.env`:

```env
COLLECTION_HOUR=0    # Hora UTC (0 = medianoche)
COLLECTION_MINUTE=0
```

Para ejecutar la colección manualmente:

```python
from scheduler import metrics_scheduler
metrics_scheduler.run_now()
```

## 🗄️ Base de Datos

Por defecto usa SQLite (`metrics.db`), pero puede configurarse PostgreSQL:

```env
# SQLite
DATABASE_URL=sqlite:///./metrics.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/metrics_db
```

### Modelos de Datos

1. **WeatherMetric**: Temperatura, humedad, presión, viento, etc.
2. **CryptoMetric**: Precio, market cap, volumen, cambio 24h, etc.
3. **NasaMetric**: APOD (título, explicación, URL de imagen, etc.)

## 🐳 Docker

### Construir imagen

```bash
docker build -t metrics-backend .
```

### Ejecutar contenedor

```bash
docker run -d \
  -p 8000:8000 \
  -e OPENWEATHER_API_KEY=tu_key \
  -e NASA_API_KEY=tu_key \
  -v $(pwd)/data:/app/data \
  --name metrics-backend \
  metrics-backend
```

## 🧪 Testing

Probar endpoints manualmente:

```bash
# Health check
curl http://localhost:8000/health

# Colectar datos del clima
curl -X POST http://localhost:8000/api/weather/collect

# Obtener últimos datos
curl http://localhost:8000/api/weather/latest
curl http://localhost:8000/api/crypto/latest
curl http://localhost:8000/api/nasa/latest

# Estadísticas
curl http://localhost:8000/api/stats/summary
```

## 📊 APIs Utilizadas

1. **OpenWeatherMap** (https://openweathermap.org/api)
   - Datos actuales del clima
   - Gratuita: 1,000 llamadas/día

2. **CoinGecko** (https://www.coingecko.com/api/documentation)
   - Precios de criptomonedas
   - Gratuita: Sin límites para uso básico

3. **NASA APOD** (https://api.nasa.gov/)
   - Astronomy Picture of the Day
   - Gratuita: 1,000 llamadas/hora con API key

## 🔧 Configuración Avanzada

### Cambiar ubicación por defecto

```env
DEFAULT_CITY=Bucaramanga
DEFAULT_COUNTRY=CO
DEFAULT_LAT=7.1254
DEFAULT_LON=-73.1198
```

### Configurar CORS

```env
ALLOWED_ORIGINS=["http://localhost:3000", "https://tudominio.com"]
```

### Logging

Los logs se imprimen en stdout con formato:

```
2025-10-30 12:00:00 - scheduler - INFO - Colectando datos del clima...
```

## 🐛 Solución de Problemas

### Error: "No API key provided"

Asegúrate de tener el archivo `.env` con las API keys correctas.

### Error de base de datos

Si usas SQLite, asegúrate de que el directorio tenga permisos de escritura.

### Scheduler no ejecuta

Verifica que `COLLECTION_HOUR` y `COLLECTION_MINUTE` estén en formato UTC.

## 📝 Próximos Pasos

1. ✅ Backend completo funcionando
2. ⏭️ Desarrollar frontend con Chart.js
3. ⏭️ Configurar Docker Compose
4. ⏭️ Implementar CI/CD
5. ⏭️ Documentación completa

## 📄 Licencia

MIT
