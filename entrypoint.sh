#!/bin/sh

# entrypoint.sh - migrations, collectstatic helper for container start
# This script is executed inside the image by default, but compose services override the CMD to start gunicorn/daphne.
set -e

# wait for DB
if [ "$DATABASE_HOST" ]; then
  echo "Waiting for database $DATABASE_HOST..."
  until nc -z "$DATABASE_HOST" "${DATABASE_PORT:-5432}"; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
  done
fi

# Run migrations and collectstatic once (safe to run multiple times)
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
