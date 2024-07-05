#!/bin/sh

WORKERS=${WORKERS:-4}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
DEBUG=${DEBUG:-false}

if [ "$DEBUG" = "True" ]; then
  adev runserver /srv/schedulr --app-factory start_app --host "$HOST" --port "$PORT"
else
  exec gunicorn schedulr.app:start_app -w "$WORKERS" -k aiohttp.GunicornWebWorker -b "$HOST":"$PORT"
fi