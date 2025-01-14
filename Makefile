CONTAINER_FRONT = angular

start-dev: env
	docker compose -f docker-compose.dev.yml up

stop-dev:
	docker compose -f docker-compose.dev.yml down

clean-dev: stop-dev
	docker volume rm postgres-volume-dev || true
	rm .env

clean-prod: stop-prod
	docker volume rm postgres-volume-prod | true
	docker volume rm uploads-volume-prod | true
	rm .env

re: clean-dev start-dev

start-prod: build-prod env
	docker compose -f docker-compose.prod.yml up

stop-prod:
	docker compose -f docker-compose.prod.yml down

build-prod: env
	docker compose -f docker-compose.prod.yml build

env:
	@if [ ! -e .env ]; then \
		printf "$(GREEN)Generate environment variables\n$(DEFAULT)"; \
		sh create-env.sh; \
	fi

cmd-dev:
	docker exec -it $(CONTAINER_FRONT) sh

cmd-prod:
	docker exec -it $(CONTAINER_FRONT)-prod sh


dump:
	docker exec postgres-dev pg_dump --dbname=$(shell grep DATABASE_URL= .env | sed 's/DATABASE_URL=//') > postgres-init/dump.sql


pr:
	@firefox https://github.com/t-h2o/matcha/pull/new/$(shell git rev-parse --abbrev-ref HEAD)
	@git cliff origin/main..HEAD -o pr-description.md || docker run -t -v "$(shell pwd)":/app/ "orhunp/git-cliff" origin/main..HEAD -o pr-description.md
	@cp pr-description.md commit-description.md
	@sed -i 's/## //' commit-description.md
	@sed -i 's/*//g' commit-description.md


.PHONY: env start-dev stop-dev start-prod stop-prod build-prod cmd-dev cmd-prod
