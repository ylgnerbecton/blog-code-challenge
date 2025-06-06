VENV=.venv/bin/activate

install:
	poetry install
	poetry run pre-commit install

run:
	poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload

lint:
	@echo "Running pre-commit hooks..."
	poetry run pre-commit run --all-files --show-diff-on-failure || true

format:
	poetry run black .

test:
	poetry run pytest --cov=app tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.pytest_cache" -exec rm -rf {} +

.PHONY: install run lint format test clean
