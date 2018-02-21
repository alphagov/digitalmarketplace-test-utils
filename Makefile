SHELL := /bin/bash
VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && virtualenv -p python3 venv || true

.PHONY: requirements-dev
requirements-dev: virtualenv requirements.txt
	${VIRTUALENV_ROOT}/bin/pip install -r requirements.txt

.PHONY: test
test: show-environment test-flake8

.PHONY: test-flake8
test-flake8: virtualenv requirements-dev
	${VIRTUALENV_ROOT}/bin/flake8 .

.PHONY: show-environment
show-environment:
	@echo "Environment variables in use:"
	@env | grep DM_ || true

