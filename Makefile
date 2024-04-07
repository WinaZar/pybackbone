migrations-%: url = postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}?sslmode=disable

.PHONY: install-hooks
install-hooks:
	@pre-commit install -t pre-commit -t commit-msg

.PHONY: lint
lint:
	@poetry run ruff check ./src ./tests
	@poetry run mypy ./src ./tests

.PHONY: dev-up
dev-up:
	@docker compose -f docker-compose.yaml up -d

.PHONY: migrations-generate
migrations-generate:
	@atlas migrate diff --env sqlalchemy

.PHONY: migrations-apply
migrations-apply:
	@atlas migrate apply --env sqlalchemy -u $(url)

.PHONY: migrations-status
migrations-status:
	@atlas migrate status --env sqlalchemy -u $(url)

.PHONY: run-web
run-web:
	@poetry run python -m src run-web

.PHONY: run-tests
run-tests:
	@poetry run pytest -v .

.PHONY: build-image
build-image:
	@docker buildx build --platform=linux/amd64 -t example:$(tag) .
