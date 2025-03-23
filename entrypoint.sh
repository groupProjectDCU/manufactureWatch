#!/bin/bash

set -e

while ! nc -z $DB_HOST $DB_PORT; do
    echo "Waiting for database connection..."
    sleep 1
done

# If no arguments are provided, run the default behavior
if [ $# -eq 0 ]; then
    echo "Database connected, applying migrations..."
    python manage.py migrate
    
    echo "Migrations applied, starting server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    # If arguments are provided, run those instead
    echo "Database connected, running custom command..."
    exec "$@"
fi