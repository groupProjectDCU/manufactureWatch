#!/bin/bash

set -e

while ! nc -z $DB_HOST $DB_PORT; do
    echo "Waiting for database connection..."
    sleep 1
done

echo "Database connected, applying migrations..."
python manage.py migrate

echo "Migrations applied, starting server..."
python manage.py runserver 0.0.0.0:8000