SHELL := /bin/bash
.DEFAULT_GOAL := help

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

# WARNING – this will wipe your host machine's db
# TODO – name the docker images and volumes instead of
# relying on the auto-generated "product-engineer-starter" prefix
remove-db-volume:
	docker volume rm product-engineer-starter_postgres_data

start: build up build-migrations migrate

help:
	@echo "Available commands:"
	@echo "  build          	Build the Docker images for the backend."
	@echo "  up             	Start the backend and database services."
	@echo "  down           	Stop and remove containers, networks, images, and volumes."
	@echo "  logs           	Follow log output for the backend."
	@echo "  migrate        	Run database migrations to the latest version."
	@echo "  build-migrations	Generate new migration file(s) for any database schema changes."

.PHONY: build up down logs migrate build-migrations help start