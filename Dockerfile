FROM python:3.11-slim

WORKDIR /app

# Copiar requirements desde backend
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh .
COPY . .

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["./start.sh"]
