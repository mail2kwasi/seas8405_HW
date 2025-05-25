#!/bin/bash
echo "Setting up IAM architecture..."

docker-compose down -v
docker-compose up --build -d

echo "Setup complete. Visit Flask App at http://localhost:5000"
