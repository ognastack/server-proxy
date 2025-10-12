PROJECT_NAME=server-proxy

up:
	docker compose -p $(PROJECT_NAME) up -d

down:
	docker compose -p $(PROJECT_NAME) down -v

restart:
	docker compose -p $(PROJECT_NAME) down
	docker compose -p $(PROJECT_NAME) up -d
