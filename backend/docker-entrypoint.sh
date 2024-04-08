#!/bin/sh
# docker-entrypoint.sh

# Exit on error
set -e

# Wait for Postgres to be ready...
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL to start"
  sleep 1
done

# Start FastAPI application with Uvicorn
# Default to port 8000 if not specified
NEXT_PUBLIC_SERVER_PORT=${NEXT_PUBLIC_SERVER_PORT:-8000}

echo "Starting Uvicorn on port $NEXT_PUBLIC_SERVER_PORT"
exec uvicorn app.main:app --host ${NEXT_PUBLIC_SERVER_HOST} --port ${NEXT_PUBLIC_SERVER_PORT} --reload