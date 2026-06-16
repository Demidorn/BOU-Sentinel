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
```
├── backend/
│   ├── app/
│   │   ├── api/             # API Endpoints (Inflation, Fraud, Systemic, Chatbot)
│   │   ├── core/            # Redis & DB Connection clients
│   │   └── main.py          # FastAPI Gateway / ASGI Socket.IO Broker
│   ├── Dockerfile
│   └── requirements.txt
├── chatbot/
│   └── chatbot_chain.py     # Multilingual Fin-Literacy Mapping Matrix
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js 14 App Router (Pages & Routes)
│   │   └── components/      # UI Layout Elements, Maps, Charts
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── ml/
│   ├── models/              # Exported Trained Binary Files (*.pkl)
│   ├── fraud_detector.py    # XGBoost Topography Evaluator
│   ├── generate_demo_data.py# Synthetic TimescaleDB Ingestion Factory
│   └── inflation_predictor.py# Meta Prophet Core Predictor
├── docker-compose.yml       # Complete Infrastructure Orchestration Manifest
├── Makefile                 # Unified Macro Operational Command Shortcuts
└── README.md
```
## 🎓 **Hackathon Status Affirmation**
*This project is fully designed and functional within isolated execution sandboxes. It represents a highly deployable, production-ready blueprint leveraging cutting-edge web and AI architectures specifically tailored to support the Bank of Uganda's long-term macro-prudential oversight objectives.*

**Authors**
* Ikilai Doreen - [Demidorn](https://github.com/Demidorn)
* Arnaud Bandonkeye - []()
* Kakooza Vianney - []()
