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
	@echo "\033[32mrun-dev-app\033[0m\t\tRun the development version (i.e. reloading) of the (FastAPI) app"
	@echo "\033[32mrun-alembic\033[0m\t\tRun alembic upgrade head"
	@echo "\033[32mrun-app\033[0m\t\t\tRun the production version of the (FastAPI) app"
	@echo "\033[32minstall-dev-app\033[0m\t\tInstall dependencies for development version of the app"
	@echo "\033[32minstall-app\033[0m\t\tInstall dependencies for production version of the app"
	@echo "\033[32mbuild-image\033[0m\t\tBuild a Docker image with the specified TAG"
	@echo "\033[32mcompose-up\033[0m\t\tStart the Docker Compose services"
	@echo "\033[32mcompose-down\033[0m\t\tStop the Docker Compose services"

.PHONY: repl
repl:
	@if [ -z "${APP_DATABASE_URL}" ]; then \
		echo "APP_DATABASE_URL is not set. Exiting."; \
		exit 1; \
	fi
	@DATABASE_URL=${APP_DATABASE_URL} poetry run ipython

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
		--env POSTGRES_DB=images \
		--env POSTGRES_PASSWORD=postgres \
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

.PHONY: run-dev-app
run-dev-app:
	@if [ -z "${APP_DATABASE_URL}" ]; then \
		echo "APP_DATABASE_URL is not set. Exiting."; \
		exit 1; \
	fi
	@DATABASE_URL=${APP_DATABASE_URL} poetry run fastapi dev src/images/endpoints/app.py

.PHONY: run-alembic
run-alembic:
	@if [ -z "${APP_DATABASE_URL}" ]; then \
		echo "APP_DATABASE_URL is not set. Exiting."; \
		exit 1; \
	fi
	@DATABASE_URL=${APP_DATABASE_URL} poetry run alembic upgrade head

.PHONY: run-app
run-app: run-alembic
	@if [ -z "${APP_DATABASE_URL}" ]; then \
		echo "APP_DATABASE_URL is not set. Exiting."; \
		exit 1; \
	fi
	@DATABASE_URL=${APP_DATABASE_URL} poetry run fastapi run src/images/endpoints/app.py

.PHONY: install-dev-app
install-dev-app:
	@poetry install --with=dev

.PHONY: install-app
install-app:
	@poetry install

.PHONY: build-image
build-image:
	@if [ -z "${TAG}" ]; then \
		echo "TAG unset. Exiting."; \
		exit 1; \
	fi
	@docker build --tag $(TAG) .

.PHONY: compose-up
compose-up:
	@if [ -z "${POSTGRES_PASSWORD}" ]; then \
		echo "Error: POSTGRES_PASSWORD is not set. Exiting."; \
		exit 1; \
	fi
	@if [ -z "${TAG}" ]; then \
		echo "Error: TAG is not set. Exiting."; \
		exit 1; \
	fi
	@docker-compose up

.PHONY: compose-down
compose-down:
	@if [ -z "${TAG}" ]; then \
		echo "Error: TAG is not set. Exiting."; \
		exit 1; \
	fi
	@docker-compose down