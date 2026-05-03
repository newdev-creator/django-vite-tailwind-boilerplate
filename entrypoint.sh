#!/bin/bash

set -e

echo "--> Création du dossier data..."
mkdir -p /app/data

echo "--> Application des migrations..."
python manage.py migrate --noinput

echo "--> Démarrage de Gunicorn..."
# Utilise la variable PORT de Coolify ou 8000 par défaut
exec gunicorn settings.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --access-logfile -
