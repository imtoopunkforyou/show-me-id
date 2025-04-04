# === Сonfiguration ===
MAKEFLAGS += --silent
make:
	cat -n ./Makefile

# === Vars ===
COMPOSE_FILE=./compose.yml
CONTAINER_NAME=smid

# === Build ====
dc-build:
	docker-compose -f $(COMPOSE_FILE) up -d --build
dc-watch:
	docker-compose -f $(COMPOSE_FILE) watch
dc-up:
	docker-compose -f $(COMPOSE_FILE) up
dc-down:
	docker-compose -f $(COMPOSE_FILE) down

# === Logs ====
logs:
	docker logs $(CONTAINER_NAME)
logs-f:
	docker logs -f $(CONTAINER_NAME)

# === Dev ===
lint:
	uv run flake8 ./smid && uv run mypy ./smid --no-pretty
pre-commit:
	uv run isort ./smid && uv run make lint

# === Aliases ===
pc: pre-commit
