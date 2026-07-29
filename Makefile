install:
	pip install -r requirements-dev.txt

test:
	pytest

lint:
	black --check src tests
	flake8 src tests

format:
	black src tests

run:
	python -m src.pipeline
