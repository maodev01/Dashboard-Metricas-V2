# Guía de Despliegue - Dashboard de Métricas

Esta guía cubre todos los escenarios de despliegue del Dashboard de Métricas.

## 📋 Tabla de Contenidos

1. [Pre-requisitos](#pre-requisitos)
2. [Despliegue Local con Docker](#despliegue-local-con-docker)
3. [Despliegue en Servidor (VPS)](#despliegue-en-servidor-vps)
4. [Despliegue en Cloud (AWS/GCP/Azure)](#despliegue-en-cloud)
5. [Configuración de CI/CD](#configuración-de-cicd)
6. [Monitoreo y Logs](#monitoreo-y-logs)
7. [Troubleshooting](#troubleshooting)

---

## Pre-requisitos

### Software Necesario

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Git** >= 2.30
- **Make** (opcional, para usar Makefile)

### API Keys Requeridas

1. **OpenWeatherMap**: https://openweathermap.org/api
   - Crear cuenta gratuita
   - Obtener API key
   
2. **NASA**: https://api.nasa.gov/
   - Obtener API key (o usar DEMO_KEY con límites)

---

## Despliegue Local con Docker

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/dashboard-metrics.git
cd dashboard-metrics
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
nano .env  # O usar tu editor preferido
```

Editar `.env` con tus API keys:

```env
OPENWEATHER_API_KEY=tu_api_key_aqui
NASA_API_KEY=tu_nasa_key_o_DEMO_KEY
```

### 3. Levantar Servicios

```bash
# Opción 1: Usando Make
make build
make up

# Opción 2: Docker Compose directo
docker-compose build
docker-compose up -d
```

### 4. Verificar Despliegue

```bash
# Ver logs
docker-compose logs -f

# Verificar salud
make health

# O manualmente
curl http://localhost:8000/health
curl http://localhost/
```

### 5. Acceder a los Servicios

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (usuario: admin@metrics.local, pass: admin)

---

## Despliegue en Servidor (VPS)

### Requisitos del Servidor

- **OS**: Ubuntu 22.04 LTS (recomendado)
- **RAM**: Mínimo 2GB (4GB recomendado)
- **Disco**: 20GB
- **CPU**: 2 cores

### 1. Preparar el Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Instalar herramientas adicionales
sudo apt install -y git make nginx certbot python3-certbot-nginx
```

### 2. Clonar y Configurar

```bash
# Crear directorio de aplicación
sudo mkdir -p /opt/dashboard-metrics
sudo chown $USER:$USER /opt/dashboard-metrics
cd /opt/dashboard-metrics

# Clonar repositorio
git clone https://github.com/tu-usuario/dashboard-metrics.git .

# Configurar environment
cp .env.example .env
nano .env
```

### 3. Configurar Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/dashboard-metrics
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Activar configuración:

```bash
sudo ln -s /etc/nginx/sites-available/dashboard-metrics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Configurar SSL con Let's Encrypt

```bash
sudo certbot --nginx -d tu-dominio.com
```

### 5. Levantar Servicios

```bash
cd /opt/dashboard-metrics
docker-compose up -d
```

### 6. Configurar como Servicio Systemd (Opcional)

```bash
sudo nano /etc/systemd/system/dashboard-metrics.service
```

Contenido:

```ini
[Unit]
Description=Dashboard Metrics
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/dashboard-metrics
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Activar:

```bash
sudo systemctl enable dashboard-metrics
sudo systemctl start dashboard-metrics
```

---

## Despliegue en Cloud

### AWS (EC2 + RDS)

#### 1. Crear Instancia EC2

- **Tipo**: t3.medium
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 30GB gp3
- **Security Group**: 
  - Permitir puertos 22, 80, 443
  - Permitir 8000 desde tu IP (para testing)

#### 2. Crear RDS PostgreSQL

- **Engine**: PostgreSQL 15
- **Instance**: db.t3.micro (dev) / db.t3.small (prod)
- **Storage**: 20GB
- **Public Access**: No
- **Security Group**: Permitir puerto 5432 desde EC2

#### 3. Configurar EC2

```bash
# Conectar a EC2
ssh -i tu-key.pem ubuntu@ec2-ip-address

# Seguir pasos de "Despliegue en Servidor"
# Usar RDS endpoint en DATABASE_URL
DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/metrics_db
```

### Google Cloud Platform (GCP)

#### 1. Crear VM Instance

```bash
gcloud compute instances create dashboard-metrics \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --tags=http-server,https-server
```

#### 2. Crear Cloud SQL PostgreSQL

```bash
gcloud sql instances create metrics-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1
```

#### 3. Desplegar Aplicación

Seguir pasos similares a AWS, usando Cloud SQL proxy para la conexión.

---

## Configuración de CI/CD

### GitHub Actions

Los workflows están en `.github/workflows/ci-cd.yml`

#### 1. Configurar Secrets en GitHub

Ir a Settings > Secrets and variables > Actions y agregar:

```
DOCKER_USERNAME
DOCKER_PASSWORD
SERVER_HOST
SERVER_USER
SSH_PRIVATE_KEY
PRODUCTION_URL
```

#### 2. SSH Key para Deploy

```bash
# Generar key
ssh-keygen -t rsa -b 4096 -C "github-actions"

# Agregar public key al servidor
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# Copiar private key a GitHub Secrets
cat ~/.ssh/id_rsa
```

#### 3. Trigger Deployment

```bash
# Push a main activa el deploy automático
git push origin main
```

### GitLab CI

Crear `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - cd backend
    - pip install -r requirements.txt
    - pytest

build:
  stage: build
  script:
    - docker build -t backend ./backend

deploy:
  stage: deploy
  only:
    - main
  script:
    - ssh user@server 'cd /opt/dashboard && git pull && docker-compose up -d'
```

---

## Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo últimas 100 líneas
docker-compose logs --tail=100
```

### Configurar Logrotate

```bash
sudo nano /etc/logrotate.d/docker
```

```
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  size=10M
  missingok
  delaycompress
  copytruncate
}
```

### Monitoreo con Prometheus + Grafana (Opcional)

Agregar a `docker-compose.yml`:

```yaml
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

---

## Backup y Restore

### Backup Automático Diario

```bash
# Crear script de backup
sudo nano /usr/local/bin/backup-metrics.sh
```

```bash
#!/bin/bash
BACKUP_DIR=/backups/dashboard-metrics
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup de PostgreSQL
docker-compose exec -T db pg_dump -U metrics_user metrics_db > $BACKUP_DIR/db_$DATE.sql

# Backup de volúmenes
docker run --rm -v metrics_postgres_data:/data -v $BACKUP_DIR:/backup ubuntu tar czf /backup/data_$DATE.tar.gz /data

# Mantener solo últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Configurar cron:

```bash
sudo crontab -e
# Agregar línea para backup diario a las 2 AM
0 2 * * * /usr/local/bin/backup-metrics.sh
```

### Restore desde Backup

```bash
# Restaurar base de datos
docker-compose exec -T db psql -U metrics_user metrics_db < backup_20241030.sql
```

---

## Troubleshooting

### Backend no inicia

```bash
# Verificar logs
docker-compose logs backend

# Verificar variables de entorno
docker-compose exec backend env

# Reiniciar servicio
docker-compose restart backend
```

### Frontend no carga

```bash
# Verificar nginx
docker-compose logs frontend

# Verificar conexión con backend
docker-compose exec frontend wget -O- http://backend:8000/health
```

### Base de datos no conecta

```bash
# Verificar estado de PostgreSQL
docker-compose exec db pg_isready -U metrics_user

# Ver logs de DB
docker-compose logs db

# Conectar manualmente
docker-compose exec db psql -U metrics_user -d metrics_db
```

### Scheduler no ejecuta

```bash
# Verificar logs del backend
docker-compose logs backend | grep scheduler

# Ejecutar colección manual
curl -X POST http://localhost:8000/api/weather/collect
```

### Problemas de SSL

```bash
# Renovar certificado Let's Encrypt
sudo certbot renew

# Verificar configuración nginx
sudo nginx -t
```

---

## Seguridad

### Checklist de Seguridad

- [ ] Cambiar contraseñas por defecto
- [ ] Configurar firewall (ufw)
- [ ] Habilitar SSL/TLS
- [ ] Limitar acceso a puertos
- [ ] Actualizar regularmente
- [ ] Configurar backups automáticos
- [ ] Monitorear logs de acceso
- [ ] Implementar rate limiting

### Configurar Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## Actualizaciones

### Actualizar Aplicación

```bash
cd /opt/dashboard-metrics
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

### Rollback

```bash
# Volver a commit anterior
git log --oneline  # Ver commits
git checkout <commit-hash>
docker-compose up -d --build
```

---

## Contacto y Soporte

Para problemas o preguntas:
- Abrir issue en GitHub
- Email: support@example.com

---

**Última actualización**: Octubre 2024