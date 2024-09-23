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
	flake8 ./smid && mypy ./smid --no-pretty
pre-commit:
	isort ./smid && make lint

# === Aliases ===
pc: pre-commit
