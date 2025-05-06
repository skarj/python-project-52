MANAGE := uv run python manage.py

.PHONY: test
test:
	@$(MANAGE) test

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
	uv run ruff check task_manager --fix

.PHONY: build
build:
	./build.sh

.PHONY: render-start
render-start:
	gunicorn task_manager.wsgi

.PHONY: dev-start
dev-start:
	@$(MANAGE) runserver
