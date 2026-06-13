#!/usr/bin/env bash
set -euo pipefail

command -v docker >/dev/null || { echo "Docker required"; exit 1; }

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env"
fi

docker compose build
docker compose up -d

docker compose exec backend python manage.py migrate --noinput

echo "Platform is running"
