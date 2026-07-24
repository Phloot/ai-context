UV ?= uv
BASE ?= HEAD

.DEFAULT_GOAL := help

.PHONY: help setup schemas schemas-check validate validate-base test lint growth check

help:
	@echo "make setup                Create .venv and sync dependencies with uv"
	@echo "make schemas              Generate JSON Schemas from CUE"
	@echo "make schemas-check        Check CUE, manifests, and generated schema drift"
	@echo "make validate             Validate the complete catalog"
	@echo "make validate-base BASE=  Validate version changes against a Git revision"
	@echo "make test                 Run the catalog test suite"
	@echo "make lint                 Run Ruff lint and formatting checks"
	@echo "make growth               Check changed Python file growth"
	@echo "make check BASE=HEAD      Run all non-mutating checks"

setup:
	$(UV) sync

schemas:
	$(UV) run python scripts/generate_schemas.py

schemas-check:
	$(UV) run python scripts/generate_schemas.py --check

validate:
	$(UV) run python scripts/validate_catalog.py

validate-base:
	$(UV) run python scripts/validate_catalog.py --base "$(BASE)"

test:
	$(UV) run python -m unittest discover -s tests -v

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

growth:
	$(UV) run python skills/maintainable-code/scripts/check_file_growth.py --base "$(BASE)"

check: schemas-check validate validate-base test lint growth
