#!/bin/bash
set -e

# TestBot Setup Script for FastAPI RealWorld Example App

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"

echo "Building Docker images..."
docker compose build

echo "Starting services..."
docker compose up -d

echo "Waiting for service to be healthy..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:8000/api/articles > /dev/null 2>&1; then
    echo "App is healthy"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "ERROR: App failed to become healthy"
    docker compose logs app
    exit 1
  fi
  sleep 2
done

echo "Registering test user..."
REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  --data-raw '{"user":{"email":"testbot@example.com","username":"testbot","password":"TestPass123!"}}')
HTTP_CODE=$(echo "$REGISTER_RESPONSE" | tail -1)
BODY=$(echo "$REGISTER_RESPONSE" | sed '$d')

TOKEN=$(echo "$BODY" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
  echo "$TOKEN" > "$SCRIPT_DIR/.auth-token"
  echo "Auth token saved"
else
  echo "WARNING: Could not extract token from registration response"
  echo "$BODY"
fi

echo "Checking container status..."
docker compose ps

echo "Setup complete"
