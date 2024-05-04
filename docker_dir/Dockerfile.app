FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev \
    postgresql-dev

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "run.py" ]