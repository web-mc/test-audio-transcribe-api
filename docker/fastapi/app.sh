#!/bin/bash

uv run alembic upgrade head
uv run gunicorn app.main:app -c /fastapi/app/configs/gunicorn.conf.py
