PROJECT_NAME=server-proxy


up-prod:
	docker compose -p $(PROJECT_NAME) up -f docker-certificates.yaml -d
	docker compose -p $(PROJECT_NAME) up -f docker-compose.yaml -d

up:
	docker compose -p $(PROJECT_NAME) up -d

down:
	docker compose -p $(PROJECT_NAME) down -v

restart:
	docker compose -p $(PROJECT_NAME) down
	docker compose -p $(PROJECT_NAME) up -d
