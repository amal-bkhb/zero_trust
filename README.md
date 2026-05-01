# Simple Zero Trust Microservices Study Project

This repository provides a very small 3-service architecture for local security and Zero Trust experiments.

## Services

- **frontend** (`frontend/`): Flask app serving a basic web page.
- **backend** (`backend/`): Flask API that reads one row from PostgreSQL.
- **database** (`database/`): PostgreSQL service initialized with one sample record.

## Communication Flow

1. User opens `http://localhost:5000` (frontend).
2. Frontend calls its own `/api/backend-status` endpoint.
3. Frontend service forwards request to backend at `http://backend:5001/api/data`.
4. Backend connects to PostgreSQL (`database:5432`) and reads data from `notes` table.
5. Backend returns JSON to frontend, frontend returns JSON to browser.

## Folder Structure

```text
.
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── database/
│   ├── Dockerfile
│   └── init.sql
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       └── index.html
├── docker-compose.yml
└── README.md
```

## Docker Support

Each service has its own Dockerfile:
- `frontend/Dockerfile`
- `backend/Dockerfile`
- `database/Dockerfile`

`docker-compose.yml` runs all services together and uses Docker service names for communication:
- Frontend -> Backend: `http://backend:5001`
- Backend -> Database: `database:5432`

## Run Locally with Docker

```bash
docker compose up --build
```

Then open:
- Frontend UI: `http://localhost:5000`
- Backend API directly: `http://localhost:5001/api/data`

## Stop

```bash
docker compose down
```
