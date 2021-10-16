.PHONY: setup-dev test unittest lint fmt

setup-dev: requirements.txt requirements_dev.txt
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt -r requirements_dev.txt
	pre-commit install

unittest:
	pytest tests/

unittest-not-slow:
	pytest -k 'not slow' --durations=5 tests/

lint:
	pylint .

# Run unittests then linting
test: unittest lint

fmt:
	black .

sort:
	isort .