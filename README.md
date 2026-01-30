# Mini SIEM Platform

A mini Security Information and Event Management platform with log collection, security analysis, alerting, and a real-time web dashboard.

## Architecture

```
Log Sources -> Python Collector -> Security Analyzer -> Database (PostgreSQL) -> FastAPI -> React Dashboard
                                                       -> Elasticsearch / Kibana
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Elasticsearch
- **Frontend**: React (Vite), ESLint
- **Monitoring**: Elasticsearch / Kibana

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.app.main:app --reload --port 8000
```

### Ingest demo logs

```bash
python backend/scripts/demo_ingest.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/logs/` | Ingest a log |
| `GET` | `/api/v1/logs/` | List logs (filter by source, severity, ip) |
| `GET` | `/api/v1/logs/search/?q=` | Search logs |
| `POST` | `/api/v1/alerts/` | Create alert |
| `GET` | `/api/v1/alerts/` | List alerts |
| `GET` | `/api/v1/stats/` | Dashboard statistics |

## License

MIT

