#!/bin/bash
echo "Starting backend on port: ${PORT}"

# Ejecuta FastAPI desde la carpeta backend
uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}
