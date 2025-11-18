# 📊 Dashboard de Métricas en Tiempo Real

Dashboard interactivo con actualización automática cada 2 minutos para visualizar datos de clima, criptomonedas y estado del transporte público de Londres.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Auto Update](https://img.shields.io/badge/Auto%20Update-2%20min-orange)

---

## ✨ Características Principales

### 📡 Fuentes de Datos en Tiempo Real
- **🌤️ Clima**: Datos meteorológicos actuales de OpenWeatherMap
- **💰 Criptomonedas**: Precios y market cap en tiempo real de CoinGecko
- **🚇 TfL Transport**: Estado del metro de Londres (Transport for London API)

### ⚡ Actualización Automática
- **Cada 2 minutos**: Colección automática de todas las métricas
- **Auto-refresh frontend**: Actualización visual sin recargar página
- **Histórico completo**: Almacenamiento de todos los datos para análisis

### 📊 Visualizaciones Interactivas
- Gráficos de líneas múltiples con Chart.js
- Tarjetas de estado en tiempo real
- Indicadores de salud por colores
- Diseño responsive para todos los dispositivos

### 🎨 Interfaz Moderna
- Diseño limpio con Tailwind CSS
- Animaciones suaves y efectos hover
- Notificaciones toast informativas
- Selector de rango de fechas para análisis histórico

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker >= 20.10
- Docker Compose >= 2.0
- API Key de OpenWeatherMap (gratuita)

### Instalación en 3 Pasos
```bash
# 1. Clonar repositorio
git clone https://github.com/TU-USUARIO/dashboard-metrics.git
cd dashboard-metrics

# 2. Configurar API key
cp .env.example .env
nano .env  # Agregar OPENWEATHER_API_KEY

# 3. Levantar servicios
docker-compose up -d
```

### Acceder a la Aplicación

- **Frontend**: http://localhost
- **API Backend**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (user: admin@metrics.local, pass: admin)

---

## 📁 Estructura del Proyecto
```
dashboard-metrics/
├── backend/                 # API FastAPI
│   ├── collectors/         # Colectores de datos
│   │   ├── weather.py     # OpenWeatherMap
│   │   ├── crypto.py      # CoinGecko
│   │   └── tfl.py         # Transport for London
│   ├── tests/             # Tests unitarios
│   ├── main.py            # Aplicación principal
│   ├── models.py          # Modelos SQLAlchemy
│   ├── routes.py          # Endpoints API
│   ├── scheduler.py       # Colección cada 2 min
│   └── requirements.txt
│
├── frontend/              # Interfaz web
│   ├── js/
│   │   ├── config.js     # Configuración
│   │   ├── api.js        # Cliente API
│   │   ├── charts.js     # Gráficos Chart.js
│   │   └── dashboard.js  # Lógica principal
│   └── index.html
│
├── nginx/                 # Reverse proxy
├── docs/                  # Documentación
│   ├── DEPLOYMENT.md     # Guía de despliegue
│   ├── ARCHITECTURE.md   # Arquitectura
│   └── API.md           # Documentación API
│
├── .github/workflows/    # CI/CD
│   └── ci-cd.yml        # Pipeline automático
│
├── docker-compose.yml    # Orquestación
├── Makefile             # Comandos útiles
└── README.md            # Este archivo
```

---

## 🔧 Configuración

### Variables de Entorno

Editar `.env`:
```env
# API Keys
OPENWEATHER_API_KEY=tu_key_aqui

# Database
DATABASE_URL=postgresql://metrics_user:metrics_password_2024@db:5432/metrics_db

# Application
DEBUG=False
ALLOWED_ORIGINS=["*"]

# Location
DEFAULT_CITY=Bucaramanga
DEFAULT_COUNTRY=CO

# Auto-Update (minutos)
COLLECTION_INTERVAL_MINUTES=2
```

### Personalizar Intervalo de Actualización

Para cambiar la frecuencia de actualización:
```env
# Actualización cada 5 minutos
COLLECTION_INTERVAL_MINUTES=5

# Actualización cada 30 segundos (no recomendado)
COLLECTION_INTERVAL_MINUTES=0.5
```

---

## 📊 APIs Utilizadas

### 1. OpenWeatherMap API
- **URL**: https://openweathermap.org/api
- **Costo**: Gratuita (1,000 llamadas/día)
- **Datos**: Temperatura, humedad, presión, viento
- **Requiere API Key**: ✅ Sí

### 2. CoinGecko API
- **URL**: https://www.coingecko.com/api/documentation
- **Costo**: Gratuita (sin límites básicos)
- **Datos**: Precios, market cap, volumen 24h
- **Requiere API Key**: ❌ No

### 3. Transport for London API
- **URL**: https://api.tfl.gov.uk/
- **Costo**: Completamente gratuita
- **Datos**: Estado de líneas de metro, BikePoints
- **Requiere API Key**: ❌ No

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

# Base de datos
make db-shell         # Acceder a PostgreSQL
make db-backup        # Crear backup
make db-restore       # Restaurar backup

# Utilidades
make health           # Verificar salud
make collect-data     # Colectar datos manualmente
make stats            # Ver estadísticas
```

### Endpoints de la API

#### Weather (Clima)
```bash
GET  /api/weather/latest
GET  /api/weather/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
POST /api/weather/collect
```

#### Crypto (Criptomonedas)
```bash
GET  /api/crypto/latest
GET  /api/crypto/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
POST /api/crypto/collect
```

#### TfL (Transport for London)
```bash
GET  /api/tfl/latest
GET  /api/tfl/line/{line_id}
GET  /api/tfl/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
GET  /api/tfl/bikes
POST /api/tfl/collect
```

#### Stats (Estadísticas)
```bash
GET  /api/stats/summary
```

---

## 🧪 Testing
```bash
# Ejecutar todos los tests
cd backend
pytest

# Con cobertura
pytest --cov=. --cov-report=html

# Ver reporte
open htmlcov/index.html
```

**Cobertura actual**: >80%

---

## 🚢 Despliegue

### Despliegue Local (Docker)
```bash
docker-compose up -d
```

### Despliegue en Servidor VPS

Ver guía completa: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
```bash
# En el servidor
git clone https://github.com/TU-USUARIO/dashboard-metrics.git
cd dashboard-metrics
cp .env.example .env
nano .env  # Configurar API key
docker-compose up -d
```

### CI/CD Automático

El proyecto incluye pipeline de GitHub Actions que:
1. ✅ Verifica código (linting)
2. ✅ Ejecuta tests automáticos
3. ✅ Construye imágenes Docker
4. ✅ Escanea vulnerabilidades
5. ✅ Despliega a producción (en push a main)

Ver: [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)

---

## 🏗️ Arquitectura
```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────┐     ┌──────────────┐
│    Nginx    │────▶│   FastAPI    │
│  (Frontend) │     │   Backend    │
└─────────────┘     └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
       ┌─────────────┐          ┌────────────┐
       │ PostgreSQL  │          │ Scheduler  │
       │  Database   │          │ (2 min)    │
       └─────────────┘          └─────┬──────┘
                                      │
                              ┌───────┴────────┐
                              ↓                ↓
                        External APIs    TfL API
                     (Weather, Crypto)
```

Ver documentación completa: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📈 Características Técnicas

### Backend
- **Framework**: FastAPI 0.104
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Scheduler**: APScheduler 3.10
- **Validación**: Pydantic 2.5

### Frontend
- **Gráficos**: Chart.js 4.4
- **Estilos**: Tailwind CSS 3.x
- **Iconos**: Font Awesome 6.4
- **JavaScript**: Vanilla ES6+

### DevOps
- **Containerización**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **CI/CD**: GitHub Actions
- **Monitoring**: Logs estructurados

---

## 🔄 Flujo de Actualización

1. **Cada 2 minutos** el scheduler ejecuta:
```
   Scheduler → Collectors → External APIs → Database
```

2. **Frontend auto-refresh**:
```
   setInterval(120s) → API Request → Update UI
```

3. **Manual trigger**:
```
   User Click → POST /collect → Immediate Update
```

---

## 📝 Changelog

### v2.0.0 (2025-11-04) - Actualización Mayor
- ✨ Migración de NASA API a TfL API
- ⚡ Actualización automática cada 2 minutos
- 🔄 Auto-refresh del frontend
- 🚇 Estado en tiempo real del metro de Londres
- 📊 Nuevas visualizaciones de estado de líneas
- 🎨 UI mejorada con indicadores en tiempo real

### v1.0.0 (2025-10-30) - Lanzamiento Inicial
- ✅ Backend completo con FastAPI
- ✅ Frontend con Chart.js
- ✅ Docker Compose
- ✅ CI/CD con GitHub Actions
- ✅ 3 fuentes de datos

---

## 🐛 Troubleshooting

### Backend no inicia
```bash
docker-compose logs backend
# Verificar API key en .env
```

### Frontend no carga datos
```bash
# Verificar CORS en config.py
# Verificar URL de API en frontend/js/config.js
```

### Auto-refresh no funciona
```bash
# Verificar en consola del navegador (F12)
# Debería aparecer: "🔄 Auto-refresh activado cada 120 segundos"
```

### Scheduler no ejecuta
```bash
docker-compose logs backend | grep "scheduler"
# Verificar COLLECTION_INTERVAL_MINUTES en .env
```

Más soluciones: [docs/DEPLOYMENT.md#troubleshooting](docs/DEPLOYMENT.md#troubleshooting)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Tu Nombre**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
- Email: tu-email@ejemplo.com
- Portfolio: https://tu-portfolio.com

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend
- [Chart.js](https://www.chartjs.org/) - Gráficos interactivos
- [Tailwind CSS](https://tailwindcss.com/) - Framework de estilos
- [OpenWeatherMap](https://openweathermap.org/) - API de clima
- [CoinGecko](https://www.coingecko.com/) - API de criptomonedas
- [Transport for London](https://api.tfl.gov.uk/) - API de transporte público

---

## ⭐ Star History

Si este proyecto te fue útil, considera darle una estrella ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=TU-USUARIO/dashboard-metrics&type=Date)](https://star-history.com/#TU-USUARIO/dashboard-metrics&Date)

---

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~6,000
- **Archivos**: 25+
- **Cobertura de tests**: >80%
- **Tiempo de actualización**: 2 minutos
- **APIs integradas**: 3

---

**Made with ❤️ using FastAPI, Chart.js and Tailwind CSS**

**Actualización en tiempo real cada 2 minutos** ⚡