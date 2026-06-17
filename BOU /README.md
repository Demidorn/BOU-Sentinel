# BOU Sentinel 🛡️

> **An AI-Powered National Economic Monitoring & Financial Security Platform**  
> Developed for the Bank of Uganda 60th Anniversary Hackathon (June 2026).

BOU Sentinel is an institutional-grade early warning framework designed to monitor systemic macroeconomic threats, detect illicit financial networks, and accelerate grassroots financial literacy across Uganda. By combining predictive machine learning models, real-time telemetry streaming, and multilingual retrieval-augmented generation (RAG), BOU Sentinel provides an executive-level cockpit for safeguarding national economic stability.

---

## 🚀 Key Innovation Capabilities

*   **📈 Macroeconomic Inflation Predictor:** Leveraging Meta Prophet to ingest volatile commodity metrics (e.g., fuel indices, exchange rate yield variances) to project headline inflation tracks up to four months out.
*   **🕵️ Illicit Capital Flight Intelligence:** A high-throughput structural risk engine using XGBoost and NetworkX graph topologies to isolate complex, multi-node mobile money laundering networks and anomalous cross-border liquidations.
*   **📊 Localized Stress Topography:** A real-time data visualizer pushing live regional risk indexes from FastAPI over WebSockets (Socket.IO) straight onto an interactive geographic command interface.
*   **🤖 Multilingual Literacy Agent:** A localized conversational safety layer acting as an SMS-gateway backend to protect retail consumers against predatory mobile loan syndicates and phishing traps in **English, Luganda, and Swahili**.

---

## Tech Stack
 
| Layer | Technology |
|---|---|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, shadcn/ui |
| Backend | Python 3.11, FastAPI, SQLAlchemy (async), Alembic |
| Database | PostgreSQL (PostGIS) |
| Cache / Queue | Redis, Celery |
| ML / Data | Prophet, scikit-learn, pandas, numpy, shap |
| Containerisation | Docker, Docker Compose |
 
---
 


Project Structure

---

## 📐 System Architecture

The platform is designed as an decoupled, multi-module stack optimized for deployment over Docker orchestrations:

┌─────────────────────────────────────────┐
              │          Next.js 14 Dashboard           │
              │   (Tailwind CSS + Tremor + Leaflet)     │
              └────────────────────┬────────────────────┘
                                   │ 
             REST APIs / WebSockets│ (Socket.IO Live Telemetry)
                                   ▼
              ┌─────────────────────────────────────────┐
              │           FastAPI Core Server           │
              └──────┬─────────────┬─────────────┬──────┘
                     │             │             │
    Timescale / SQL  │     Cache / │      Vector │ Semantic
    Queries          │     PubSub  │      Search │ Engine
                     ▼             ▼             ▼
┌─────────────────────────┐   ┌───────────┐   ┌───────────┐
│  TimescaleDB (Postgres) │   │   Redis   │   │  ChromaDB │
│ (Time-Series Metrics)   │   │  Broker   │   │  Vector   │
└─────────────────────────┘   └─────┬─────┘   └───────────┘
│
▼
┌───────────────────────────┐
│    Celery Background      │
│     Worker (UBOS)         │
└───────────────────────────┘


---

## Prerequisites
 
Make sure you have the following installed:
 
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 20+](https://nodejs.org/)
- [pnpm](https://pnpm.io/installation) — `npm install -g pnpm`
---
 
## Getting Started
 
### 1. Clone the repository
 
```bash
git clone https://github.com/Demidorn/BOU-Sentinel.git
cd BOU-Sentinel
```
 
### 2. Set up environment variables
 
```bash
cp .env.example .env
```
 
Edit `.env` and fill in your values:
 
```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/bou_sentinel
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=bou_sentinel
 
# Redis
REDIS_URL=redis://localhost:6379
 
# FastAPI
SECRET_KEY=your-secret-key-here
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
 
# Next.js
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```
 
---
 
## Running the Project
 
There are two ways to run the project — with Docker (recommended for first run) or locally with a virtual environment (recommended for day-to-day development).
 
---
 
### Option A — Docker (everything in containers)
 
Starts Postgres, Redis, the API, and the web app all at once.
 
```bash
make up
```
apply  migrations  to your PostgreSQL container
```bash
make migrate
```
Inject your mock financial datasets
```bash
make seed
```

| Service | URL |
|---|---|
| Web | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
 
Stop everything:
 
```bash
make down
```
 
---
 
### Option B — Local development with virtual environment (recommended)
 
This runs only Postgres and Redis in Docker, while the API and web run natively — much lighter on resources.
 
#### Step 1 — Start only the database services
 
```bash
make dev-services
```
 
This starts Postgres and Redis containers only.
 
#### Step 2 — Set up the Python virtual environment
 
```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate        # Linux / Mac
# or
.venv\Scripts\activate           # Windows
```
 
#### Step 3 — Install Python dependencies
 
For core API dependencies only (faster):
 
```bash
pip install -r requirements.txt
```
 
For full install including ML packages (Prophet, scikit-learn, shap — takes longer):
 
```bash
pip install -r requirements-ml.txt
```
 
> **Note:** `prophet` compiles C++ code via `pystan` during install — this is expected and can take a few minutes.
 
#### Step 4 — Install frontend dependencies
 
```bash
cd apps/web
pnpm install
```
 
#### Step 5 — Run database migrations
 
```bash
# from root
make migrate
```
 
#### Step 6 — Start the dev servers
 
```bash
# from root — starts both API and web concurrently
make dev
```
 
Or start them individually:
 
```bash
make dev-api    # FastAPI on http://localhost:8000
make dev-web    # Next.js on http://localhost:3000
```
 
---
 
## Adding shadcn Components
 
With dependencies installed, add components from the shadcn registry:
 
```bash
cd apps/web
npx shadcn@latest add button
npx shadcn@latest add card table dialog dropdown-menu toast
```
 
---
 
## Database Migrations
 
Create a new migration after changing a model:
 
```bash
make migrate-create name="add_alerts_table"
```
 
Apply all pending migrations:
 
```bash
make migrate
```
 
---
 
## Seed Data
 
Populate the database with initial data:
 
```bash
make seed
```
 
---
 
## Makefile Reference
 
| Command | Description |
|---|---|
| `make up` | Start all services in Docker |
| `make down` | Stop all Docker services |
| `make dev` | Start API + web locally (requires venv) |
| `make dev-api` | Start FastAPI locally only |
| `make dev-web` | Start Next.js locally only |
| `make dev-services` | Start only Postgres + Redis in Docker |
| `make migrate` | Run all pending DB migrations |
| `make migrate-create name=".."` | Create a new migration |
| `make seed` | Seed the database |
| `make forecast` | Run forecast script manually |
| `make logs` | Tail all Docker logs |
| `make logs-api` | Tail API logs only |
| `make logs-web` | Tail web logs only |
| `make shell-api` | Open a bash shell in the API container |
| `make shell-db` | Open psql in the Postgres container |
| `make lint` | Lint API (ruff) and web (eslint) |
| `make format` | Format API (ruff) and web (prettier) |
| `make test` | Run all tests |
| `make build` | Build Docker images only |
 
---
 
## Common Issues
 
**`fatal: destination path 'BOU-Sentinel' already exists and is not an empty directory`**
The repo was already cloned. Just navigate into it and pull:
```bash
cd BOU-Sentinel && git pull
```
 
**`Cannot find module 'next'` or similar TypeScript errors**
Dependencies aren't installed yet:
```bash
cd apps/web && pnpm install
```
Then restart the TypeScript server in VS Code: `Ctrl+Shift+P` → "TypeScript: Restart TS Server".
 
**`Module '@/lib/utils' has no exported member 'X'`**
The type isn't defined yet. Add it to `apps/web/lib/types.ts` and import from there:
```ts
import type { Alert } from "@/lib/types";
```
 
**`process` is not defined (TypeScript)**
Install Node types:
```bash
cd apps/web && pnpm add -D @types/node
```
 
**`prophet` install is very slow**
This is expected — it compiles C++ via `pystan`. Let it run. Use `requirements.txt` (without ML) for faster installs when you don't need forecasting.
 
---
 
## Development Tips
 
- Use `make dev-services` + `make dev` for the lightest local setup — Docker only runs the two DB containers.
- The `.venv` folder lives inside `apps/api/` and is gitignored — never commit it.
- All `NEXT_PUBLIC_*` env vars are inlined at build time — changes require a server restart.
- Use `lib/types.ts` for all shared TypeScript types and `lib/utils.ts` for utility functions only.
- API auto-docs are available at `http://localhost:8000/docs` (Swagger) and `/redoc`.
---
 

## 👥 Hackathon Squad Core Task Distribution

To maximize speed and depth during the hackathon sprint, responsibilities are cleanly isolated across a 3-person pipeline layout:

### 🎨 Person 1: Frontend Architecture & Command UI
*   Assembled the **Next.js 14 App Router** interface using TypeScript and an institutional dark-mode grid layout.
*   Implemented responsive time-series predictive runways via **Recharts** and high-density KPI metrics using **Tremor UI**.
*   Engineered the **Leaflet OpenStreetMap visual canvas** mapping live localized macro risk nodes across administrative Ugandan corridors.
*   Wired up client-side **Socket.IO stream intercepts** to capture live pipeline server anomalies without interface refreshes.

### 🔌 Person 2: Core API Gateway & Distributed Infrastructure
*   Engineered the asynchronous **FastAPI service core** organizing cross-functional routing schemas.
*   Implemented native **Socket.IO ASGI app server loops** to broadcast parallel real-time regional risk vectors.
*   Configured **Docker Compose orchestration** networking multi-system runtimes (PostgreSQL, Redis, ChromaDB).
*   Integrated **Celery background workers** on Redis brokers to handle heavy analytical loops separate from primary HTTP routes.

### 🧠 Person 3: Data Telemetry Machine Learning Pipelines
*   Constructed a synthetic macroeconomic data factory populating time-series parameters into hypertable structures.
*   Built and serialized the **Meta Prophet Forecaster** engine managing structural price regressions.
*   Programmed the fraud evaluation routine feeding topological inputs (`velocity_30m`, `routing_risk`) into a optimized **XGBoost Classifier**.
*   Structured the **multilingual financial literacy heuristic tree** acting as the RAG prototype engine mapping native dialects.

---

## 🛠️ Instant Setup & Replication Runway

Ensure you have `Docker` and `Docker Compose` installed.

### 1. Environmental Setup
Initialize your local configurations from the provided infrastructure blueprint:
```bash
make setup
```

### 2. Stand Up Core Infrastructure Containers
Spin up the database engines, backend services, worker instances, and UI framework concurrently:

```Bash
make build
make up
```
### 3. Hydrate & Train Machine Learning Engines
Once all container health-checks report optimal operation, execute the data seeding script followed by the model compilation routines from your secondary terminal layout:

```Bash
# Ingest synthetic macro parameters and transactional logs into TimescaleDB
make seed

# Execute compilation passes to output production .pkl binaries to the ML volume
make train
```
### 4. System Verification Interfaces
__Executive Web Dashboard Node: ```http://localhost:3000```__

__Interactive Core API Documentation Explorer: ```http://localhost:8010/docs```__


**Repository Structural Topology**


## 🎓 **Hackathon Status Affirmation**
*This project is fully designed and functional within isolated execution sandboxes. It represents a highly deployable, production-ready blueprint leveraging cutting-edge web and AI architectures specifically tailored to support the Bank of Uganda's long-term macro-prudential oversight objectives.*

**Authors**
* Ikilai Doreen - [Demidorn](https://github.com/Demidorn)
* Arnaud Bandonkeye - []()
* Kakooza Vianney - []()
