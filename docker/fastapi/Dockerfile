# Зависимости
FROM python:3.13-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev  --no-install-project


# Приложение
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /fastapi

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

RUN chmod a+x /fastapi/docker/fastapi/app.sh
