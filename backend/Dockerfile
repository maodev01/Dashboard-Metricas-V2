FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del backend
COPY ../backend/ .

ENV PYTHONPATH=/app

# Railway asigna PORT automáticamente
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
