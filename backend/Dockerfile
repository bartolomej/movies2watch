FROM python:3.8-alpine

WORKDIR /app

RUN apk add build-base postgresql-dev
RUN pip3 install flask flask_cors psycopg2 numpy cerberus requests_futures

COPY . ./

CMD ["python3", "src/server.py"]