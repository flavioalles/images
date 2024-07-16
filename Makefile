.PHONY: format-code
format-code:
	@poetry run black --safe --config pyproject.toml .

.PHONY: check-typing
check-typing:
	@poetry run mypy --config-file pyproject.toml src/