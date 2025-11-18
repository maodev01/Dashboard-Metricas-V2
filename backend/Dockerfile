FROM python:3.11-slim

WORKDIR /app

# Copiar requirements DESDE LA MISMA CARPETA donde está el Dockerfile
COPY /requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el backend completo
COPY . .

# Copiar script de arranque
RUN chmod +x start.sh

EXPOSE 8000

# Usar start.sh como único punto de entrada
CMD ["./start.sh"]
