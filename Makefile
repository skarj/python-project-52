MANAGE := uv run python manage.py

.PHONY: test
test:
	uv run pytest

.PHONY: install
install:
	@uv sync

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: collectstatic
collectstatic:
	@$(MANAGE) collectstatic --no-input

.PHONY: lint
lint:
	uv run ruff check task_manager

.PHONY: build
build:
	./build.sh
