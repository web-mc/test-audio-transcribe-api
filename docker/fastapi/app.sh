#!/bin/bash

uv run gunicorn app.main:app -c /fastapi/app/configs/gunicorn.conf.py
