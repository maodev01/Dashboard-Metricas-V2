.PHONY: help install dev build up down restart logs clean test lint format

# Variables
DOCKER_COMPOSE = docker-compose
PYTHON = python3
PIP = pip3

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==================== INSTALACIÓN ====================

install: ## Instalar dependencias del backend
	cd backend && $(PIP) install -r requirements.txt

install-dev: ## Instalar dependencias de desarrollo
	cd backend && $(PIP) install -r requirements.txt pytest pytest-cov flake8 black

# ==================== DESARROLLO ====================

dev: ## Ejecutar backend en modo desarrollo
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Ejecutar frontend en servidor local
	cd frontend && $(PYTHON) -m http.server 8080

# ==================== DOCKER ====================

build: ## Construir imágenes Docker
	$(DOCKER_COMPOSE) build

up: ## Levantar todos los servicios
	$(DOCKER_COMPOSE) up -d

down: ## Detener todos los servicios
	$(DOCKER_COMPOSE) down

restart: ## Reiniciar todos los servicios
	$(DOCKER_COMPOSE) restart

logs: ## Ver logs de todos los servicios
	$(DOCKER_COMPOSE) logs -f

logs-backend: ## Ver logs del backend
	$(DOCKER_COMPOSE) logs -f backend

logs-frontend: ## Ver logs del frontend
	$(DOCKER_COMPOSE) logs -f frontend

logs-db: ## Ver logs de la base de datos
	$(DOCKER_COMPOSE) logs -f db

# ==================== TESTING ====================

test: ## Ejecutar tests del backend
	cd backend && pytest -v

test-cov: ## Ejecutar tests con cobertura
	cd backend && pytest --cov=. --cov-report=html --cov-report=term

test-watch: ## Ejecutar tests en modo watch
	cd backend && pytest-watch

# ==================== CALIDAD DE CÓDIGO ====================

lint: ## Verificar código con flake8
	cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	cd backend && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Formatear código con black
	cd backend && black .

format-check: ## Verificar formato sin modificar
	cd backend && black --check .

# ==================== BASE DE DATOS ====================

db-shell: ## Acceder a shell de PostgreSQL
	$(DOCKER_COMPOSE) exec db psql -U metrics_user -d metrics_db

db-backup: ## Crear backup de la base de datos
	$(DOCKER_COMPOSE) exec -T db pg_dump -U metrics_user metrics_db > backup_$$(date +%Y%m%d_%H%M%S).sql

db-restore: ## Restaurar backup (usar: make db-restore FILE=backup.sql)
	$(DOCKER_COMPOSE) exec -T db psql -U metrics_user metrics_db < $(FILE)

# ==================== UTILIDADES ====================

clean: ## Limpiar archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

clean-docker: ## Limpiar containers y volúmenes
	$(DOCKER_COMPOSE) down -v
	docker system prune -af

prune: ## Limpiar imágenes y contenedores no usados
	docker system prune -af --volumes

# ==================== PRODUCCIÓN ====================

prod-up: ## Levantar servicios en producción
	$(DOCKER_COMPOSE) -f docker-compose.yml up -d --build

prod-down: ## Detener servicios de producción
	$(DOCKER_COMPOSE) -f docker-compose.yml down

prod-logs: ## Ver logs de producción
	$(DOCKER_COMPOSE) -f docker-compose.yml logs -f

# ==================== HEALTH CHECKS ====================

health: ## Verificar salud de los servicios
	@echo "Verificando Backend..."
	@curl -f http://localhost:8000/health || echo "Backend no disponible"
	@echo "\nVerificando Frontend..."
	@curl -f http://localhost/ || echo "Frontend no disponible"
	@echo "\nVerificando Base de datos..."
	@$(DOCKER_COMPOSE) exec db pg_isready -U metrics_user || echo "DB no disponible"

# ==================== DATOS ====================

collect-data: ## Colectar datos manualmente
	@curl -X POST http://localhost:8000/api/weather/collect
	@curl -X POST http://localhost:8000/api/crypto/collect
	@curl -X POST http://localhost:8000/api/nasa/collect

stats: ## Mostrar estadísticas
	@curl http://localhost:8000/api/stats/summary | python3 -m json.tool