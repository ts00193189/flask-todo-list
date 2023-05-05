SHELL := /bin/bash
PYTHON_FILE := $(shell find . -type f -name "*.py" ! -path "**/venv/**")

# if .env.example exists, use environment variable in .env.example
ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: lint \
		format \
		test \
		run-local \
		setup \
		generate-pylintrc \
		ci \
		setup \

setup:
	flask db upgrade

lint:
	pylint $(PYTHON_FILE)
	isort --check-only --diff $(PYTHON_FILE)
	autopep8 --diff --exit-code $(PYTHON_FILE)

format:
	isort $(PYTHON_FILE)
	autopep8 --in-place $(PYTHON_FILE)

test:
	flask test

run-local:
	flask run

generate-pylintrc:
	pylint --generate-rcfile > .pylintrc

ci:
	make lint
	make test
