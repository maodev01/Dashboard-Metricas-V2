FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de backend a /app
COPY backend/ .

# Copiar start.sh desde backend
COPY backend/start.sh .
RUN chmod +x start.sh

# Railway asigna el PORT automáticamente
ENV PYTHONPATH=/app

CMD ["bash", "start.sh"]
