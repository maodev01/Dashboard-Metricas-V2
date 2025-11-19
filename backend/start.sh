#!/bin/bash

# Obtener el puerto de la variable de entorno o usar 8080 por defecto
PORT=${PORT:-8080}

echo "Starting backend on port: $PORT"

# Iniciar uvicorn
uvicorn main:app --host 0.0.0.0 --port $PORT
