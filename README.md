# Simple Zero Trust Microservices Study Project

This repository provides a very small 3-service architecture for local security and Zero Trust experiments.

## Services

- **frontend** (`frontend/`): Flask app serving a basic web page.
- **backend** (`backend/`): Flask API that reads one row from PostgreSQL.
- **database** (`database/`): PostgreSQL service initialized with one sample record.

## Communication Flow


5. Backend returns JSON to frontend, frontend returns JSON to browser.

## Folder Structure

```text
.
├── backend/

├── docker-compose.yml
└── README.md
```



```bash
docker compose up --build
```

Then open:
- Frontend UI: `http://localhost:5000`
- Backend API directly: `http://localhost:5001/api/data`

