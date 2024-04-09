SHELL := /bin/bash
.DEFAULT_GOAL := help

copy-dev-env-vars:
	cp .env.sample .env
	cp ./frontend/.env.local.sample ./frontend/.env.local

build:
	docker-compose build backend frontend

up:
	docker-compose up -d

build-migrations:
	docker-compose exec backend alembic revision --autogenerate -m "generating alembic revision"

migrate:
	docker-compose exec backend alembic upgrade head

down:
	docker-compose down

be-logs:
	docker-compose logs -f backend

fe-logs:
	docker-compose logs -f frontend

db-logs:
	docker-compose logs -f db

remove-db-volume:
	docker volume rm product-engineer-starter_postgres_data

start:
	$(MAKE) copy-dev-env-vars
	$(MAKE) build
	$(MAKE) up
	@echo "Waiting for services to start up. To-do: find a deterministic way to proceed..."
	sleep 10
	$(MAKE) build-migrations
	$(MAKE) migrate

help:
	@echo "Available commands:"
	@echo "  build             Build the Docker images for the backend and frontend."
	@echo "  up                Start the backend and database services."
	@echo "  down              Stop and remove containers, networks, images, and volumes."
	@echo "  be-logs           Follow log output for the backend."
	@echo "  fe-logs           Follow log output for the frontend."
	@echo "  db-logs           Follow log output for the database."
	@echo "  build-migrations  Generate new migration file(s) for any database schema changes."
	@echo "  migrate           Run database migrations to the latest version."
	@echo "  start             Run the full application setup sequence."
	@echo "  remove-db-volume  WARNING – This will wipe your host machine's db"

.PHONY: build up down be-logs fe-logs db-logs migrate build-migrations help start remove-db-volume
