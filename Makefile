.PHONY: help
help:
	@echo "\033[1mimages\033[0m"
	@echo "\n\033[1mAvailable targets:\033[0m"
	@echo "\033[32mcheck-style\033[0m\t\tCheck code style using black"
	@echo "\033[32mformat-code\033[0m\t\tFormat code using black"
	@echo "\033[32mcheck-typing\033[0m\t\tCheck typing using mypy"

.PHONY: check-style
check-style:
	@poetry run black --safe --check --diff --color --config pyproject.toml .

.PHONY: format-code
format-code:
	@poetry run black --safe --config pyproject.toml .

.PHONY: check-typing
check-typing:
	@poetry run mypy --config-file pyproject.toml src/