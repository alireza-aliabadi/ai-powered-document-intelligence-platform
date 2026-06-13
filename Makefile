COMPOSE=docker compose

.PHONY: help up down build logs shell migrate test clean

help:
	@echo "make up build down logs shell migrate test clean"

up:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

shell:
	$(COMPOSE) exec backend bash

migrate:
	$(COMPOSE) exec backend python manage.py migrate

test:
	$(COMPOSE) exec backend pytest

clean:
	$(COMPOSE) down -v --remove-orphans
