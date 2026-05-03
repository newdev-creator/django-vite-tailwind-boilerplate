# --- Étape 1 : Construction du Frontend (Vite) ---
FROM node:22-alpine AS frontend-builder

WORKDIR /app

# Installation de pnpm
RUN npm install -g pnpm

# Copie des fichiers de dépendances frontend
COPY package.json pnpm-lock.yaml* ./

# Installation des dépendances
RUN pnpm install --frozen-lockfile

# Copie du reste du code pour le build (nécessaire pour Tailwind/Vite)
COPY . .

# Build des assets (Vite)
RUN pnpm run build

# --- Étape 2 : Environnement Python ---
FROM python:3.12-slim

# Empêche Python de créer des fichiers .pyc et assure que les logs sortent immédiatement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Installation des dépendances système (nécessaires pour psycopg2, pillow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python via uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --group prod --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Copie du code complet
COPY . .

# Récupération des assets buildés par l'étape frontend
COPY --from=frontend-builder /app/static ./static

# Script de démarrage
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


EXPOSE $PORT

ENTRYPOINT ["/app/entrypoint.sh"]
