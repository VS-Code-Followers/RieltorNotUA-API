FROM python:3.10

ENV PYTHONUNBUFFERED=1

LABEL maintainer="https://github.com/CBoYXD" version="1.0.0"

WORKDIR /usr/src/rieltor_api

RUN apt update && apt upgrade -y

COPY . /usr/src/rieltor_api

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

CMD alembic upgrade head && \
    python3 main.py