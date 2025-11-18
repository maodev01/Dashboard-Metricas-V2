# 🔐 Configuración de GitHub Secrets

Esta guía te ayudará a configurar todos los secrets necesarios para el CI/CD.

---

## 📋 Secrets Requeridos

### 1. Docker Hub

#### DOCKER_USERNAME
Tu usuario de Docker Hub

**Cómo obtenerlo:**
1. Ir a https://hub.docker.com
2. Crear cuenta o hacer login
3. Tu username es el que aparece en tu perfil

**Valor de ejemplo:**
```
tuusuario
```

#### DOCKER_PASSWORD
Tu contraseña o Access Token de Docker Hub (recomendado)

**Cómo obtenerlo:**
1. Docker Hub → Account Settings → Security
2. Click "New Access Token"
3. Nombre: "GitHub Actions"
4. Permisos: Read, Write, Delete
5. Copiar el token generado

---

### 2. Servidor de Producción

#### SERVER_HOST
IP o dominio del servidor de producción

**Valor de ejemplo:**
```
123.45.67.89
```
o
```
dashboard.tudominio.com
```

#### STAGING_HOST (opcional)
IP o dominio del servidor de staging

**Valor de ejemplo:**
```
staging.tudominio.com
```

---

### 3. SSH Key

#### SSH_PRIVATE_KEY
Llave SSH privada para conectarse al servidor

**Cómo generarla:**
```bash
# En tu máquina local (Windows PowerShell)
ssh-keygen -t rsa -b 4096 -C "github-actions" -f github-deploy

# Esto crea dos archivos:
# - github-deploy (privada) → Para GitHub Secret
# - github-deploy.pub (pública) → Para el servidor
```

**En el servidor:**
```bash
# Agregar llave pública al servidor
ssh tu-usuario@tu-servidor
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
# Pegar contenido de github-deploy.pub
chmod 600 ~/.ssh/authorized_keys
```

**En GitHub:**
```bash
# Copiar contenido de la llave PRIVADA
cat github-deploy

# Pegar TODO el contenido (incluyendo -----BEGIN y -----END)
```

---

### 4. API Keys

#### OPENWEATHER_API_KEY
Tu API key de OpenWeatherMap

**Cómo obtenerla:**
1. Ir a https://openweathermap.org/api
2. Sign Up / Sign In
3. API Keys → Generar nueva key
4. Copiar la key

**Valor de ejemplo:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

### 5. Notificaciones (Opcional)

#### SLACK_WEBHOOK
Webhook para notificaciones en Slack

**Cómo obtenerlo:**
1. Ir a https://api.slack.com/apps
2. Create New App → From scratch
3. Nombre: "Dashboard Metrics CI/CD"
4. Seleccionar workspace
5. Incoming Webhooks → Activate
6. Add New Webhook to Workspace
7. Seleccionar canal (#deployments)
8. Copiar Webhook URL

**Valor de ejemplo:**
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX
```

#### K6_CLOUD_TOKEN (Opcional)
Token para tests de performance con k6 Cloud

---

## 🔧 Cómo Agregar Secrets en GitHub

1. Ir a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Nombre: (ej: `DOCKER_USERNAME`)
5. Value: (pegar el valor)
6. Click **"Add secret"**
7. Repetir para cada secret

---

## ✅ Checklist de Secrets

### Producción (Requeridos)
- [ ] `DOCKER_USERNAME`
- [ ] `DOCKER_PASSWORD`
- [ ] `SERVER_HOST`
- [ ] `SSH_PRIVATE_KEY`
- [ ] `OPENWEATHER_API_KEY`

### Staging (Opcional)
- [ ] `STAGING_HOST`

### Notificaciones (Opcional)
- [ ] `SLACK_WEBHOOK`
- [ ] `K6_CLOUD_TOKEN`

---

## 🧪 Probar Secrets

Después de agregar los secrets, haz un commit pequeño para activar el workflow:
```bash
git add .
git commit -m "test: verificar CI/CD"
git push origin main
```

Ve a **Actions** en GitHub y verifica que el workflow se ejecute correctamente.

---

## 🔒 Seguridad

**NUNCA** expongas tus secrets:
- ❌ No los commitees en `.env`
- ❌ No los pongas en código
- ❌ No los compartas en screenshots
- ✅ Usa solo GitHub Secrets
- ✅ Rota las keys periódicamente
- ✅ Usa diferentes keys para staging/prod

---

## 🆘 Troubleshooting

### Error: "SSH connection failed"
- Verificar que SSH_PRIVATE_KEY esté completa (con -----BEGIN y -----END)
- Verificar que la llave pública esté en `~/.ssh/authorized_keys` del servidor
- Verificar permisos: `chmod 600 ~/.ssh/authorized_keys`

### Error: "Docker login failed"
- Verificar DOCKER_USERNAME y DOCKER_PASSWORD
- Si usas 2FA, debes usar un Access Token, no tu contraseña

### Error: "API key invalid"
- Verificar que OPENWEATHER_API_KEY sea válida
- Probar manualmente: `curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=TU_KEY"`

---

**Última actualización**: 2025-11-04
