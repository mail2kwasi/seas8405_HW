up:
	docker-compose up --build

down:
	docker-compose down -v

logs:
	docker-compose logs -f

build:
	docker compose build

# @echo "waiting for keycloak to start..."
# 	sleep 20
# 	./setup-keycloak-user.sh

start:
	docker compose up -d
	

stop:
	docker compose down

clean:
	docker system prune -f

restart: stop start

show:
	docker compose ps
