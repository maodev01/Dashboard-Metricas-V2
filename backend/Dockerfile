FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde el MISMO directorio backend
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar start.sh
COPY start.sh .
RUN chmod +x start.sh

# Copiar TODO el backend al contenedor
COPY . .

# Exponemos el puerto que Railway usa
EXPOSE 8000

# Comando de inicio (Railway inyecta $PORT como número)
CMD ["./start.sh"]
