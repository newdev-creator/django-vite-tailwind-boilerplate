# ==============================================================================
# BoilerPlat — Makefile
# ==============================================================================

.PHONY: help dev dev-build dev-down dev-logs dev-ps dev-shell \
        prod-build prod-up prod-down prod-logs \
        migrate makemigrations createsuperuser shell \
        lint format test collectstatic

# Affiche l'aide par défaut
help:
	@echo ""
	@echo "  BoilerPlat — Commandes disponibles"
	@echo "  ─────────────────────────────────────────────────────"
	@echo ""
	@echo "  DEV"
	@echo "    make dev              Démarrer l'environnement de dev"
	@echo "    make dev-build        Build + démarrer l'environnement de dev"
	@echo "    make dev-down         Stopper l'environnement de dev"
	@echo "    make dev-logs         Afficher les logs dev en temps réel"
	@echo "    make dev-ps           État des containers dev"
	@echo "    make dev-shell        Ouvrir un shell dans le container Django"
	@echo ""
	@echo "  PROD"
	@echo "    make prod-build       Build l'image de production"
	@echo "    make prod-up          Démarrer la production (docker-compose.yml)"
	@echo "    make prod-down        Stopper la production"
	@echo "    make prod-logs        Afficher les logs prod en temps réel"
	@echo ""
	@echo "  DJANGO"
	@echo "    make migrate          Appliquer les migrations"
	@echo "    make mm app=<app>     Créer les migrations pour une app"
	@echo "    make superuser        Créer un superutilisateur"
	@echo "    make shell            Ouvrir le shell Django"
	@echo "    make collectstatic    Collecter les fichiers statiques"
	@echo ""
	@echo "  QUALITÉ"
	@echo "    make lint             Vérifier le code (ruff)"
	@echo "    make format           Formater le code (ruff format)"
	@echo "    make test             Lancer les tests"
	@echo ""

# ==============================================================================
# DEV
# ==============================================================================

dev:
	docker compose -f dev.docker-compose.yml up

dev-build:
	docker compose -f dev.docker-compose.yml up --build

dev-down:
	docker compose -f dev.docker-compose.yml down

dev-logs:
	docker compose -f dev.docker-compose.yml logs -f

dev-ps:
	docker compose -f dev.docker-compose.yml ps

dev-shell:
	docker exec -it BoilerPlat-dev bash

# ==============================================================================
# PROD
# ==============================================================================

prod-build:
	docker compose up --build -d

prod-up:
	docker compose up -d

prod-down:
	docker compose down

prod-logs:
	docker compose logs -f

# ==============================================================================
# DJANGO (exécutés dans le container dev)
# ==============================================================================

migrate:
	docker exec BoilerPlat-dev .venv/bin/python manage.py migrate

mm:
	docker exec BoilerPlat-dev .venv/bin/python manage.py makemigrations $(app)

superuser:
	docker exec -it BoilerPlat-dev .venv/bin/python manage.py createsuperuser

shell:
	docker exec -it BoilerPlat-dev .venv/bin/python manage.py shell

collectstatic:
	docker exec BoilerPlat-dev .venv/bin/python manage.py collectstatic --noinput

# ==============================================================================
# QUALITÉ
# ==============================================================================

lint:
	docker exec BoilerPlat-dev .venv/bin/ruff check .

format:
	docker exec BoilerPlat-dev .venv/bin/ruff format .

test:
	docker exec BoilerPlat-dev .venv/bin/python manage.py test apps.accounts apps.files apps.folders
