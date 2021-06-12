default:
	@echo "See usage in Makefile"

.PHONY: sys-deps install run format lint
sys-deps:
	pip install -U pre-commit "poetry>=1,<2" "tox>=3,<4" "tox-docker>=3,<4"
	pre-commit install

install:
	poetry install

run:
	poetry run python app.py

LINT_TARGETS = snake/ app.py

format:
	poetry run black $(LINT_TARGETS)
	poetry run autoflake --in-place --remove-all-unused-imports -r $(LINT_TARGETS)
	poetry run isort --trailing-comma -rc $(LINT_TARGETS)

lint:
	poetry run flake8 $(LINT_TARGETS)
