#!/bin/sh

echo "Starting backend on port: ${PORT:-8000}"

uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
