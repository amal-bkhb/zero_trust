# Simple Zero Trust Microservices Study Project

This repository provides a very small 3-service architecture for local security and Zero Trust experiments.

## Services

- **frontend** (`frontend/`): Flask app serving a basic web page.
- **backend** (`backend/`): Flask API that reads one row from PostgreSQL.
- **database** (`database/`): PostgreSQL service initialized with one sample record.

## Communication Flow

1. User opens the frontend.
2. Frontend calls its own `/api/backend-status` endpoint.
3. Frontend forwards request to backend at `http://backend:5001/api/data`.
4. Backend connects to PostgreSQL at `database:5432` and reads from `notes` table.
5. Backend returns JSON to frontend, frontend returns JSON to browser.

## Folder Structure

```text
.
├── backend/
├── database/
├── frontend/
├── k8s/
│   ├── backend-deployment.yaml
│   ├── database-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── security/
│       ├── 00-default-deny-all.yaml
│       ├── 10-allow-frontend-to-backend.yaml
│       └── 20-allow-backend-to-database.yaml
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

### Run Locally with Docker

```bash
docker compose up --build
```

Then open:
- Frontend UI: `http://localhost:5000`
- Backend API directly: `http://localhost:5001/api/data`

Stop:

```bash
docker compose down
```

## Kubernetes Manifests (Minikube)

The `k8s/` folder contains simple Deployment + Service manifests for all three services:
- `frontend` (Service type: **NodePort**)
- `backend` (Service type: **ClusterIP**)
- `database` (Service type: **ClusterIP**)

### Deploy on Minikube

1. Start Minikube:

```bash
minikube start
```

2. Build images into Minikube's Docker daemon:

```bash
eval $(minikube docker-env)
docker build -t zero-trust-frontend:latest ./frontend
docker build -t zero-trust-backend:latest ./backend
```

3. Apply Kubernetes manifests:

```bash
kubectl apply -f k8s/
```

4. Check resources:

```bash
kubectl get pods
kubectl get svc
```

5. Open frontend in your browser:

```bash
minikube service frontend
```

## Zero Trust NetworkPolicies

Policies in `k8s/security/` implement a simple Zero Trust model:

- Deny all ingress and egress by default.
- Allow only:
  - frontend -> backend on TCP 5001
  - backend -> database on TCP 5432
- Therefore blocked paths include:
  - frontend -> database
  - database -> frontend
  - database -> internet

### Apply policies

```bash
kubectl apply -f k8s/security/
```

### Test policies

Run a temporary test pod with networking tools:

```bash
kubectl run net-test --image=nicolaka/netshoot --restart=Never -it --rm -- /bin/bash
```

Inside the pod, run:

```bash
# should succeed
curl -s http://backend:5001/api/data

# should fail (frontend->database is blocked by policy design)
nc -zv database 5432

# should fail from database pods to internet; test with pod-targeted command below
```

Verify database-style egress is blocked by running a temporary pod with label `app=database`:

```bash
kubectl run db-egress-test --image=nicolaka/netshoot --labels app=database --restart=Never -it --rm -- nc -zv 1.1.1.1 80
```

Remove policies if needed:

```bash
kubectl delete -f k8s/security/
```

This project intentionally does **not** include Istio yet.
