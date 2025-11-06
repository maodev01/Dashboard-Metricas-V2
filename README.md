# 📊 Dashboard de Métricas

Dashboard completo para visualizar y analizar métricas de clima, criptomonedas y datos astronómicos de NASA APOD. Sistema automatizado con colección diaria de datos y visualizaciones interactivas.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Características

### 📡 Fuentes de Datos
- **🌤️ Clima**: Datos en tiempo real y históricos de OpenWeatherMap
- **💰 Criptomonedas**: Precios, market cap y volúmenes de CoinGecko
- **🚀 NASA APOD**: Astronomy Picture of the Day con imágenes HD

### 📊 Visualizaciones
- Gráficos interactivos con Chart.js
- Múltiples líneas de tiempo y comparaciones
- Cards informativos con datos actuales
- Diseño responsive para todos los dispositivos

### 🤖 Automatización
- Colección automática diaria de datos
- Scheduler configurable (APScheduler)
- Almacenamiento histórico en PostgreSQL
- Endpoints para colección manual

### 🎨 Interfaz Moderna
- Diseño limpio con Tailwind CSS
- Animaciones suaves y efectos hover
- Selector de rango de fechas
- Notificaciones en tiempo real

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker >= 20.10
- Docker Compose >= 2.0
- API Keys (gratuitas):
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [NASA](https://api.nasa.gov/) (opcional, usar DEMO_KEY)

### Instalación en 3 Pasos

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/dashboard-metrics.git
cd dashboard-metrics

# 2. Configurar variables de entorno
cp .env.example .env
nano .env  # Agregar tus API keys

# 3. Levantar servicios
docker-compose up -d
```

### Acceder a la Aplicación

- **Frontend**: http://localhost
- **API Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050

---

## 📁 Estructura del Proyecto

```
dashboard-metrics/
├── backend/                 # API FastAPI
│   ├── collectors/         # Colectores de datos
│   │   ├── weather.py
│   │   ├── crypto.py
│   │   └── nasa.py
│   ├── tests/              # Tests unitarios
│   ├── main.py             # Aplicación principal
│   ├── models.py           # Modelos SQLAlchemy
│   ├── routes.py           # Endpoints API
│   ├── scheduler.py        # Tareas programadas
│   └── requirements.txt
│
├── frontend/               # Interfaz web
│   ├── js/
│   │   ├── config.js      # Configuración
│   │   ├── api.js         # Cliente API
│   │   ├── charts.js      # Gráficos
│   │   └── dashboard.js   # Lógica principal
│   └── index.html
│
├── nginx/                  # Configuración Nginx
├── docs/                   # Documentación
│   ├── DEPLOYMENT.md      # Guía de despliegue
│   └── ARCHITECTURE.md    # Arquitectura del sistema
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # Pipeline CI/CD
│
├── docker-compose.yml      # Orquestación Docker
├── Makefile               # Comandos útiles
└── README.md              # Este archivo
```

---

## 🛠️ Uso

### Comandos con Makefile

```bash
# Desarrollo
make dev              # Ejecutar backend en modo desarrollo
make dev-frontend     # Ejecutar frontend local

# Docker
make build            # Construir imágenes
make up               # Levantar servicios
make down             # Detener servicios
make logs             # Ver logs en tiempo real
make restart          # Reiniciar servicios

# Testing
make test             # Ejecutar tests
make test-cov         # Tests con cobertura

# Calidad de código
make lint             # Verificar con flake8
make format           # Formatear con black

# Base de datos
make db-shell         # Acceder a PostgreSQL
make db-backup        # Crear backup
make db-restore FILE=backup.sql  # Restaurar backup

# Utilidades
make health           # Verificar salud de servicios
make collect-data     # Colectar datos manualmente
make stats            # Ver estadísticas
make clean            # Limpiar archivos temporales
```

### API Endpoints

#### Weather (Clima)
```bash
GET  /api/weather/latest                    # Último registro
GET  /api/weather/daily?target_date=YYYY-MM-DD
GET  /api/weather/range?start_date=...&end_date=...
POST /api/weather/collect                   # Colectar ahora
```

#### Crypto (Criptomonedas)
```bash
GET  /api/crypto/latest                     # Últimos precios
GET  /api/crypto/daily?target_date=YYYY-MM-DD&symbol=BTC
GET  /api/crypto/range?start_date=...&end_date=...&symbol=BTC
POST /api/crypto/collect                    # Colectar ahora
```

#### NASA
```bash
GET  /api/nasa/latest                       # Último APOD
GET  /api/nasa/daily?target_date=YYYY-MM-DD
GET  /api/nasa/range?start_date=...&end_date=...
POST /api/nasa/collect                      # Colectar ahora
```

#### Stats
```bash
GET  /api/stats/summary                     # Resumen general
```

---

## 🔧 Configuración

### Variables de Entorno

Editar `.env`:

```env
# API Keys
OPENWEATHER_API_KEY=tu_key_aqui
NASA_API_KEY=DEMO_KEY

# Database
DATABASE_URL=postgresql://user:pass@db:5432/metrics_db

# Application
DEBUG=False
ALLOWED_ORIGINS=["http://localhost","https://tudominio.com"]

# Location
DEFAULT_CITY=Bucaramanga
DEFAULT_COUNTRY=CO

# Scheduler (UTC)
COLLECTION_HOUR=0
COLLECTION_MINUTE=0
```

### Frontend Configuration

Editar `frontend/js/config.js`:

```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',
    DEFAULT_DAYS_RANGE: 7,
    // ... más configuraciones
};
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
cd backend
pytest

# Con cobertura
pytest --cov=. --cov-report=html

# Ver reporte de cobertura
open htmlcov/index.html
```

### Tests Incluidos

- ✅ Tests unitarios de modelos
- ✅ Tests de endpoints API
- ✅ Tests de colectores
- ✅ Tests de integración
- ✅ Coverage >80%

---

## 🚢 Despliegue

### Despliegue Local

```bash
docker-compose up -d
```

### Despliegue en Servidor

Ver guía completa: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

```bash
# En el servidor
git clone https://github.com/tu-usuario/dashboard-metrics.git
cd dashboard-metrics
cp .env.example .env
# Editar .env con tus valores
docker-compose up -d
```

### CI/CD con GitHub Actions

El proyecto incluye pipeline automático que:
1. ✅ Verifica código (linting)
2. ✅ Ejecuta tests
3. ✅ Construye imágenes Docker
4. ✅ Escanea vulnerabilidades
5. ✅ Despliega a producción (en push a main)

Ver: [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)

---

## 📊 Capturas de Pantalla

### Dashboard Principal
*Vista general con estadísticas, clima, criptomonedas y NASA APOD*

### Gráfico de Clima
*Temperatura, humedad y viento en múltiples ejes Y*

### Tarjetas de Criptomonedas
*Precios en tiempo real con cambios 24h*

---

## 🏗️ Arquitectura

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐
│  Nginx  │────▶│ FastAPI │────▶│PostgreSQL│     │ External │
│Frontend │     │ Backend │     │ Database │     │   APIs   │
└─────────┘     └─────────┘     └──────────┘     └──────────┘
                     │
                     ▼
              ┌──────────┐
              │Scheduler │
              │(APScheduler)│
              └──────────┘
```

Ver documentación completa: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Guías de Contribución

- Seguir PEP 8 para código Python
- Escribir tests para nuevas funcionalidades
- Actualizar documentación
- Usar commits descriptivos

---

## 📝 Roadmap

### v1.0 (Actual) ✅
- [x] Backend completo con FastAPI
- [x] Frontend con Chart.js y Tailwind
- [x] Docker Compose
- [x] CI/CD Pipeline
- [x] Documentación completa

### v1.1 (Próximo)
- [ ] Autenticación de usuarios
- [ ] Dashboard personalizable
- [ ] Exportar datos (CSV/PDF)
- [ ] Alertas por email

### v2.0 (Futuro)
- [ ] WebSockets para real-time
- [ ] Machine Learning predictions
- [ ] Mobile app
- [ ] API GraphQL

---

## 🐛 Troubleshooting

### Backend no inicia
```bash
docker-compose logs backend
# Verificar API keys en .env
```

### Frontend no carga datos
```bash
# Verificar CORS en config.py
# Verificar URL de API en config.js
```

### Base de datos no conecta
```bash
docker-compose exec db pg_isready -U metrics_user
docker-compose restart db
```

Más soluciones: [docs/DEPLOYMENT.md#troubleshooting](docs/DEPLOYMENT.md#troubleshooting)

---

## 📚 Documentación

- [Guía de Despliegue](docs/DEPLOYMENT.md)
- [Arquitectura del Sistema](docs/ARCHITECTURE.md)
- [Backend README](backend/README_BACKEND.md)
- [Frontend README](frontend/README_FRONTEND.md)
- [API Documentation](http://localhost:8000/docs) (cuando esté corriendo)

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend
- [Chart.js](https://www.chartjs.org/) - Gráficos
- [Tailwind CSS](https://tailwindcss.com/) - Estilos
- [OpenWeatherMap](https://openweathermap.org/) - API de clima
- [CoinGecko](https://www.coingecko.com/) - API de criptomonedas
- [NASA](https://api.nasa.gov/) - API de datos espaciales

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Tu Nombre**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@example.com

---

## ⭐ Star History

Si este proyecto te fue útil, considera darle una estrella ⭐

---

**Made with ❤️ using FastAPI, Chart.js and Tailwind CSS**