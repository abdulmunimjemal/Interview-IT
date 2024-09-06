# variables
POETRY = poetry

all: install lint test run

install: pyproject.toml
	$(POETRY) install

lint:
	$(POETRY) run flake8 app tests || (echo "Linting failed!" && exit 1)

mypy:
	$(POETRY) run mypy app tests

test:
	$(POETRY) run pytest tests

run: run.py
	$(POETRY) run python run.py

clean:
	echo "[INFO] Cleaning up"
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	echo "[INFO] Cleaned up"

distclean: clean
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

