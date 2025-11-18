#!/bin/sh
echo "Starting backend on port: ${PORT}"

# Railway siempre proporciona $PORT, solo lo usamos
exec uvicorn main:app --host 0.0.0.0 --port "${PORT}"
