#!/bin/bash

# run migrations db
poetry run alembic upgrade head

# start application
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero.app:app