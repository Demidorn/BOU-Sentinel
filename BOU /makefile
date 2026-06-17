.PHONY: up down build logs seed migrate test

# ── Start everything ─────────────────────────────
up:
	docker compose up -d --build

down:
	docker compose down

# ── Build only ───────────────────────────────────
build:
	docker compose build

# ── Logs ──────────────────────────────────────────
logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

logs-web:
	docker compose logs -f web

# ── Seed database ────────────────────────────────
seed:
	docker compose exec api python /app/scripts/seed_data.py

# ── Run forecast manually ────────────────────────
forecast:
	docker compose exec api python /app/scripts/run_forecast.py

# ── Access shell ─────────────────────────────────
shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec postgres psql -U bou_sentinel -d bou_sentinel

# ── Dev mode (without Docker) ────────────────────
dev-api:
	cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Dev mode on virtual environment (without Docker)
dev-api-venv:
	cd apps/api && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-web:
	cd apps/web && pnpm run dev

dev-services:
	docker compose up -d postgres redis


dev:
	make dev-services
	make -j2 dev-api dev-web


# ── Run database migrations ───────────────────────
migrate:
	docker compose exec api alembic upgrade head

# Example  of running a command in dev mode with virtual environment
# make dev-api-venv
# make dev-web