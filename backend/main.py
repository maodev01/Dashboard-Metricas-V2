from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from config import settings
from database import init_db
from routes import router
from scheduler import metrics_scheduler

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación
    """
    # Startup
    logger.info("Iniciando aplicación...")

    # Inicializar base de datos
    logger.info("Inicializando base de datos...")
    init_db()
    logger.info("Base de datos inicializada")

    # Iniciar scheduler
    logger.info("Iniciando scheduler de métricas...")
    metrics_scheduler.start()
    logger.info("Scheduler iniciado")

    # Colectar métricas iniciales (opcional, comentar si no se desea)
    # logger.info("Colectando métricas iniciales...")
    # metrics_scheduler.run_now()

    logger.info("Aplicación iniciada exitosamente")

    yield

    # Shutdown
    logger.info("Deteniendo aplicación...")
    metrics_scheduler.stop()
    logger.info("Aplicación detenida")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para dashboard de métricas con datos de clima, criptomonedas y NASA",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api")

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "Dashboard de Métricas API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "weather": {
                "latest": "/api/weather/latest",
                "daily": "/api/weather/daily?target_date=YYYY-MM-DD",
                "range": "/api/weather/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD",
                "collect": "/api/weather/collect (POST)"
            },
            "crypto": {
                "latest": "/api/crypto/latest",
                "daily": "/api/crypto/daily?target_date=YYYY-MM-DD&symbol=BTC",
                "range": "/api/crypto/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&symbol=BTC",
                "collect": "/api/crypto/collect (POST)"
            },
            "nasa": {
                "latest": "/api/nasa/latest",
                "daily": "/api/nasa/daily?target_date=YYYY-MM-DD",
                "range": "/api/nasa/range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD",
                "collect": "/api/nasa/collect (POST)"
            },
            "stats": {
                "summary": "/api/stats/summary"
            }
        }
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
