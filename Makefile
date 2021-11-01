.PHONY: release dev run test format clean
.DEFAULT: help

help: ## Display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Remove general artifact files
	find . -name '.coverage' -delete
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '.pytest_cache' -type d | xargs rm -rf
	find . -name '__pycache__' -type d | xargs rm -rf
	find . -name '.ipynb_checkpoints' -type d | xargs rm -rf
	if [[ ! -d "venv" ]]; then \
		rm -rf venv; \
	fi
	if [[ ! -f "requirements.txt" ]]; then \
		rm -r requirements.txt; \
	fi

format: dev ## Scan and format all files with pre-commit
	venv/bin/pre-commit run --all-files

venv: ## Create virtual environment if venv directory not present
	`which python3` -m venv venv
	venv/bin/pip install -U pip pip-tools wheel --no-cache-dir

requirements.txt: venv requirements.in ## Generate requirements for release
	venv/bin/pip-compile -o requirements.txt requirements.in

dev: requirements.txt  ## Install dependencies for dev
	venv/bin/pip-sync requirements.txt
	venv/bin/pre-commit install

run: dev ## Run with dev dependencies
	venv/bin/python -m src.main

test: dev ## Run all tests with coverage
	venv/bin/pytest tests --cov=src -v --cov-report=term-missing