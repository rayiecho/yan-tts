FROM python:3.11-slim

RUN apt-get update && apt-get install -y espeak espeak-ng && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn app2:app --bind 0.0.0.0:${PORT:-8080}
