#!/bin/bash

set -e

PROJECT_DIR="$HOME/MLH-Task-2-Team-1"

cd "$PROJECT_DIR" || exit 1

git fetch origin
git reset --hard origin/main

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build

docker compose -f docker-compose.prod.yml ps