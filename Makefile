# Scan the built image for vulnerabilities
scan:
	docker scout recommendations mywebapp:latest

# Code vulnerabilities
check:
	@echo "Running code analysis with Bandit..."
	docker run --rm -v C:/Users/mail2/seas-8405/seas-8405/week-7/container-security/before:/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
	@echo "Running dependency check with pip-audit..."
	docker run --rm -v C:/Users/mail2/seas-8405/seas-8405/week-7/container-security/before:/app python:3.9-alpine sh -c "pip install pip-audit && pip-audit -r /app/requirements.txt"


# Host config security check
host-security:
	@echo "Running Docker Bench for Security..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security

# Build Docker image after security checks
dbuild:
	docker build -t mywebapp .

# Run the container
run:
	docker run -p 6000:5000 mywebapp

# Docker Compose commands
build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker system prune -f

restart: stop start
