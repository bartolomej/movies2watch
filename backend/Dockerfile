FROM python:3.8-alpine

WORKDIR /app

RUN apk add build-base postgresql-dev
RUN pip3 install flask flask_cors psycopg2

COPY . ./

CMD ["python3", "src/server.py"]