.PHONY: format-code
format-code:
	@poetry run black --safe --config pyproject.toml .