FROM python:3.9-slim-buster

WORKDIR /app

RUN pip3 install flask flask_cors

COPY . ./

CMD ["python3", "src/server.py"]