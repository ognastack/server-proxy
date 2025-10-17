PROJECT_NAME=server-proxy


up-prod:
	docker compose -p $(PROJECT_NAME) -f docker-certificates.yaml up -d
	docker compose -p $(PROJECT_NAME) -f docker-compose.yaml up -d

up:
	docker compose -p $(PROJECT_NAME) up -d

down:
	docker compose -p $(PROJECT_NAME) down -v

restart:
	docker compose -p $(PROJECT_NAME) down
	docker compose -p $(PROJECT_NAME) up -d
