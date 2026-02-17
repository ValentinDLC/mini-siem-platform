# Mini SIEM Platform

A mini Security Information and Event Management platform with log collection, security analysis, alerting, and a real-time web dashboard.

## Architecture

```
Log Sources -> Python Collector -> Security Analyzer -> Database -> FastAPI -> React Dashboard
                                                       (PostgreSQL or SQLite) -> Elasticsearch (optional)
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL (production) / SQLite (default local)
- **Search**: Elasticsearch (optional, graceful fallback if unavailable)
- **Frontend**: React (Vite), ESLint
- **Monitoring**: Kibana (with Elasticsearch)

## Quick Start (Local with SQLite)

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

## Production (PostgreSQL + Elasticsearch)

Set environment variables (see `backend/.env.example`):

```env
DATABASE_URL=postgresql://user:password@localhost:5432/siem
ELASTICSEARCH_URL=http://localhost:9200
```

Install PostgreSQL driver:

```bash
pip install psycopg2-binary
```

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

