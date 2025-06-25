# Base image to export requirements
FROM python:3.11-slim AS requirements-stage

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
WORKDIR /tmp

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# App image
FROM python:3.11-slim AS build-stage

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /src

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-traditional && \
    apt-get install -y build-essential && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=requirements-stage /tmp/requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app ./app
COPY ./tests ./tests
