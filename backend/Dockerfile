FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar backend
COPY backend ./backend

# Copiar .env a /app
COPY .env .

COPY start.sh .
RUN chmod +x start.sh

ENV PYTHONPATH=/app

CMD ["bash", "start.sh"]
