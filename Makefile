fmt:
	poetry run black .

check:
	poetry run pytest tests
	poetry run black --check .
	poetry run flake8

run-example:
	poetry run pytest --cov=example example

clean-build:
	rm -rf dist

build: check clean-build
	poetry build

deploy: build
	./deploy.sh
