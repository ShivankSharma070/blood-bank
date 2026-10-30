FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ARG APP_VERSION=v1

COPY app/${APP_VERSION}/app.py /app/app.py

ENV DATA_FILE=/data/donors.json

RUN mkdir -p /data

EXPOSE 5000

CMD ["python", "app.py"]
