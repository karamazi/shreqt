help: ## Displays this help dialog.
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep`); \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_cmd=`echo $${help_split[0]}`; \
		help_desc=`echo $${help_split[2]}`; \
		printf "\033[36m %-15s \033[0m %s\n" $$help_cmd $$help_desc ; \
	done

fmt: ## Format code with black
	poetry run black .

check: ## Runs tests, and static analysis checks
	poetry run pytest tests
	poetry run black --check .
	poetry run flake8
	poetry run safety check --full-report

run-example: ## Runs example implementation (requires running DB)
	poetry run pytest --cov=example example

clean-build:
	rm -rf dist

build: ## Builds package
build: check clean-build
	poetry build

deploy: ## Deploys package to pypi (requires set credentials)
deploy: build
	./deploy.sh
