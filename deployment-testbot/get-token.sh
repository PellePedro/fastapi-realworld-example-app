#!/bin/bash
# TestBot Auth Token Script for FastAPI RealWorld Example App
# Returns the JWT token created during setup

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOKEN_FILE="$SCRIPT_DIR/.auth-token"

if [ -f "$TOKEN_FILE" ]; then
  cat "$TOKEN_FILE"
else
  echo "ERROR: Auth token not found. Run setup.sh first." >&2
  exit 1
fi
