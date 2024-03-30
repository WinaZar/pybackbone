.PHONY: install-hooks lint

install-hooks:
	@pre-commit install -t pre-commit -t commit-msg

lint:
	@poetry run ruff check ./src ./tests
	@poetry run mypy ./src ./tests
