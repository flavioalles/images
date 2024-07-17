.PHONY: help
help:
	@echo "\033[1mimages\033[0m"
	@echo "\n\033[1mAvailable targets:\033[0m"
	@echo "\033[32mrepl\033[0m\t\t\tStart an interactive Python shell"
	@echo "\033[32mcheck-style\033[0m\t\tCheck code style using black"
	@echo "\033[32mformat-code\033[0m\t\tFormat code using black"
	@echo "\033[32mcheck-typing\033[0m\t\tCheck typing using mypy"
	@echo "\033[32mstart-db\033[0m\t\tStart the images-db container"
	@echo "\033[32mstop-db\033[0m\t\t\tStop the images-db container"
	@echo "\033[32mconnect-db\033[0m\t\tConnect to the images-db container"
	@echo "\033[32mrun-tests\033[0m\t\tRun tests using pytest"

.PHONY: repl
repl:
	@poetry run ipython

.PHONY: check-style
check-style:
	@poetry run black --safe --check --diff --color --config pyproject.toml .

.PHONY: format-code
format-code:
	@poetry run black --safe --config pyproject.toml .

.PHONY: check-typing
check-typing:
	@poetry run mypy --config-file pyproject.toml src/

.PHONY: start-db
start-db:
	# NOTE: Using data dir. in the project root to persist data.
	# Avoiding use of privileged location (e.g. /var/lib/postgresql/data
	# or /var/lib/docker/volumes/postgresql/images/) to bypass need for
	# admin privileges.
	@mkdir -p ./data/docker/volumes/postgresql/images/
	@if [ -z "${POSTGRES_PASSWORD}" ]; then \
		echo "POSTGRES_PASSWORD is not set. Exiting."; \
		exit 1; \
	fi
	@docker run --name images-db \
		--env POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		--publish 5432:5432 \
		--rm \
		--volume ./data/docker/volumes/postgresql/images/:/var/lib/postgresql/data \
		postgres:15.7

.PHONY: stop-db
stop-db:
	@docker stop images-db

.PHONY: connect-db
connect-db:
	@docker exec -i --tty images-db psql -U postgres -p 5432 -d images

.PHONY: run-tests
run-tests:
	@if [ -z "${TEST_DATABASE_URL}" ]; then \
		echo "TEST_DATABASE_URL is not set. Exiting."; \
		exit 1; \
	fi
	@DATABASE_URL=${TEST_DATABASE_URL} poetry run pytest --verbose --cov=src/ tests/