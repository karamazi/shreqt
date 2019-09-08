
lint:
	poetry run black .


check:
	poetry run black --check .
	poetry run flake8 --max-line-length=99
	poetry run pytest --cov=shreqt/ tests

run-example:
	poetry run pytest --cov=example example

clean-build:
	rm -rf dist

build: check clean-build
	poetry build

deploy: build
	./deploy.sh
