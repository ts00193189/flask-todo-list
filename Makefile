SHELL := /bin/bash
PYTHON_FILE := $(shell find . -type f -name "*.py" ! -path "**/venv/**")

.PHONY: lint \
		format \

lint:
	pylint $(PYTHON_FILE)
	isort --check-only --diff $(PYTHON_FILE)
	autopep8 --diff --exit-code $(PYTHON_FILE)

format:
	isort $(PYTHON_FILE)
	autopep8 --in-place $(PYTHON_FILE)
