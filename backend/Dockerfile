FROM python:3.11-slim

WORKDIR /app

# Copiar requirements DESDE LA RAÍZ hacia /app dentro del contenedor
COPY ../requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el backend
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
