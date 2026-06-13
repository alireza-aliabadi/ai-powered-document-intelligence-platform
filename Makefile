.PHONY: help build up down logs migrate shell test clean createsuperuser celery-worker-logs db-shell backup restore

help:
	@echo "Available commands:"
	@echo "  make build              - Build Docker images"
	@echo "  make up                 - Start all services"
	@echo "  make down               - Stop all services"
	@echo "  make logs               - View logs from all services"
	@echo "  make logs-backend       - View backend logs"
	@echo "  make logs-celery        - View Celery worker logs"
	@echo "  make logs-frontend      - View frontend logs"
	@echo "  make logs-aistor        - View aistor logs"
	@echo "  make migrate            - Run Django migrations"
	@echo "  make createsuperuser    - Create a Django superuser"
	@echo "  make shell              - Open Django shell"
	@echo "  make test               - Run tests"
	@echo "  make clean              - Remove containers and volumes"
	@echo "  make ps                 - Show running containers"
	@echo "  make restart            - Restart all services"
	@echo "  make backup             - Backup database and volumes"
	@echo "  make restore            - Restore database from backup"
	@echo ""
	@echo "Frontend commands:"
	@echo "  make frontend-build     - Build frontend Docker image"
	@echo "  make frontend-install   - Install frontend dependencies"
	@echo "  make frontend-lint      - Run ESLint on frontend"
	@echo "  make frontend-bash      - Access frontend container shell"
	@echo "  make frontend-dev       - Start frontend in development mode (local)"
	@echo "  make frontend-preview   - Preview frontend build locally"

build:
	docker compose build --no-cache

up:
	docker compose up -d
	@echo "Services started. Waiting for health checks..."
	@sleep 5
	@docker compose ps

down:
	docker compose down

stop:
	docker compose stop

restart:
	docker compose restart

ps:
	docker compose ps

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-celery:
	docker compose logs -f celery_worker

logs-frontend:
	docker compose logs -f frontend

logs-db:
	docker compose logs -f postgres

logs-redis:
	docker compose logs -f redis

logs-mongodb:
	docker compose logs -f mongodb

logs-aistor:
	docker compose logs -f aistor

migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

shell:
	docker compose exec backend python manage.py shell

shell-plus:
	docker compose exec backend python manage.py shell_plus

test:
	docker compose exec backend python manage.py test

test-coverage:
	docker compose exec backend coverage run --source='.' manage.py test && coverage report

lint:
	docker compose exec backend ruff check .

format:
	docker compose exec backend autopep8 --in-place --aggressive --aggressive -r .

type-check:
	docker compose exec backend mypy .

clean:
	docker compose down -v
	@echo "Cleaned up containers and volumes"

clean-logs:
	docker compose exec backend rm -rf logs/*
	@echo "Cleaned up log files"

backend-bash:
	docker compose exec backend bash

frontend-bash:
	docker compose exec frontend sh

db-shell:
	docker compose exec postgres psql -U postgres -d ai_platform

redis-cli:
	docker compose exec redis redis-cli

mongo-shell:
	docker compose exec mongodb mongosh -u admin -p

aistor-console:
	@echo "Aistor console available at http://localhost:9001"

backup:
	@echo "Creating backup..."
	@mkdir -p backups
	@docker compose exec -T postgres pg_dump -U postgres -d ai_platform > backups/db_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Database backup created in backups/"

restore:
	@echo "Available backups:"
	@ls -la backups/
	@read -p "Enter backup filename: " backup_file; \
	if [ -f "$$backup_file" ]; then \
		docker compose exec -T postgres psql -U postgres -d ai_platform < $$backup_file; \
		echo "Database restored from $$backup_file"; \
	else \
		echo "Backup file not found"; \
	fi

health:
	@echo "Checking service health..."
	@docker compose exec -T postgres pg_isready -U postgres || echo "PostgreSQL: DOWN"
	@docker compose exec -T redis redis-cli ping || echo "Redis: DOWN"
	@docker compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1 && echo "MongoDB: UP" || echo "MongoDB: DOWN"
	@docker compose exec -T aistor curl -s http://localhost:9000/minio/health/live > /dev/null && echo "Aistor: UP" || echo "Aistor: DOWN"
	@docker compose ps

setup:
	@echo "Setting up project..."
	@if [ ! -f .env ]; then \
        cp .env.example .env; \
        echo "Created .env file - please update with your configuration"; \
    fi
	@chmod +x docker-setup.sh
	@make build
	@make up
	@make migrate
	@echo "Setup complete!"

dev-setup: setup
	@echo "Installing dev dependencies..."
	@docker compose exec backend poetry install --with dev

rebuild:
	docker compose down
	docker compose build --no-cache
	docker compose up -d
	@echo "Rebuilt and restarted all services"

logs-all:
	docker compose logs -f --all

pull:
	docker compose pull

version:
	docker compose version
	docker --version

# Frontend-specific commands
frontend-build:
	docker compose build --no-cache frontend

frontend-install:
	cd frontend && npm install

frontend-lint:
	cd frontend && npm run lint

frontend-fix-lint:
	cd frontend && npm run lint -- --fix

frontend-build-local:
	cd frontend && npm run build

frontend-dev:
	cd frontend && npm run dev

frontend-preview:
	cd frontend && npm run preview

frontend-bash:
	docker compose exec frontend sh

frontend-logs:
	docker compose logs -f frontend

frontend-install-deps:
	docker compose exec frontend npm install

frontend-update-deps:
	docker compose exec frontend npm update

frontend-audit:
	cd frontend && npm audit

frontend-audit-fix:
	cd frontend && npm audit fix
