FROM python:3.10

LABEL maintainer="https://github.com/CBoYXD" version="1.0.0"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/rieltor_api

RUN apt update && apt upgrade -y

COPY . /usr/src/rieltor_api

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

CMD python3 main.py