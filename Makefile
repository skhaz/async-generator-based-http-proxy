.PHONY: help deploy run tests upgrade vet

.SILENT:

SHELL := bash -eou pipefail

export PYTHONPATH=.

ifeq ($(shell command -v docker-compose;),)
	COMPOSE := docker compose
else
	COMPOSE := docker-compose
endif

help:
	awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

deploy: ## Deploy on Google Cloud Run
	gcloud config set run/region us-central1
	gcloud run deploy proxy --source $(shell pwd) --platform managed --allow-unauthenticated

run: ## Run the project using docker-compose
	$(COMPOSE) up --build

tests: vet ## Run tests
	pytest --cov=app tests/

upgrade: ## Upgrade dependencies
	pur --requirement requirements/common.txt
	pur --requirement requirements/development.txt
	pur --requirement requirements/tests.txt
	pur --requirement requirements/types.txt

vet: ## Run linters, type-checking, auto-formaters, and other tools
	bandit -r app/ tests/
	black app/ tests/
	flake8 --max-line-length=88 app/ tests/
	isort --force-single-line-imports app/ tests/
	mypy app/ tests/
