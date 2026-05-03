# Dockerfile.dev — image unique avec Python + Node pour le développement
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer Node 22 + pnpm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pnpm \
    && rm -rf /var/lib/apt/lists/*

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dépendances Python
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Dépendances Node
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

# Le code est monté via volume, pas copié ici
