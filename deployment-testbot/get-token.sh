#!/bin/bash
# Generate and return a JWT token by registering/logging in a test user

set -e

API_URL="${API_URL:-http://localhost:8000/api}"
EMAIL="testbot@example.com"
USERNAME="testbot"
PASSWORD="TestPass123!"

# Try login first (user may already exist from setup)
RESPONSE=$(curl -s -X POST "$API_URL/users/login" \
  -H "Content-Type: application/json" \
  -d "{\"user\":{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}}" 2>/dev/null)

TOKEN=$(echo "$RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# If login failed, try registering
if [ -z "$TOKEN" ]; then
  RESPONSE=$(curl -s -X POST "$API_URL/users" \
    -H "Content-Type: application/json" \
    -d "{\"user\":{\"email\":\"$EMAIL\",\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}}")

  TOKEN=$(echo "$RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
fi

if [ -z "$TOKEN" ]; then
  echo "ERROR: Could not obtain auth token" >&2
  echo "$RESPONSE" >&2
  exit 1
fi

echo "Bearer $TOKEN"
