FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /src

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-traditional && \
    apt-get install -y build-essential && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app ./app
COPY ./tests ./tests
