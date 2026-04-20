# Job Processing System - Stage 2 DevOps

A production-ready containerized microservices application consisting of a Node.js frontend, FastAPI API, Python worker, and Redis queue.

## Architecture
- **Frontend**: Node.js/Express app (Port 3000)
- **API**: FastAPI app (Port 8000)
- **Worker**: Python background processor
- **Redis**: Message queue and state store

## Prerequisites
- Docker (20.10+)
- Docker Compose (v2.0+)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kehindejejelaye/hng14-stage2-devops
   cd hng14-stage2-devops
   ```

2. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env if necessary, though defaults work for local compose
   ```

3. **Bring up the stack:**
   ```bash
   docker compose up -d --build
   ```

4. **Verify Startup:**
   Wait about 10-20 seconds for services to pass health checks.
   - Access the frontend at: `http://localhost:3000`
   - Access the API docs at: `http://localhost:8000/docs`
   
   A successful startup is indicated by all containers showing `(healthy)` when running:
   ```bash
   docker compose ps
   ```

## Development and CI/CD

### Local Testing
To run the API unit tests locally:
```bash
pip install -r api/requirements.txt pytest mock redis httpx
pytest api/test_main.py
```

### CI/CD Pipeline
The project includes a GitHub Actions pipeline (`.github/workflows/pipeline.yml`) that performs:
1. **Lint**: Python (flake8), JS (eslint), Dockerfiles (hadolint)
2. **Test**: Unit tests with coverage
3. **Build**: Docker image builds
4. **Security Scan**: Trivy vulnerability scanning
5. **Integration Test**: Full stack validation in the runner
6. **Deploy**: Scripted rolling update on pushes to `main`

## Maintenance
To tear down the stack:
```bash
docker compose down
```
To view logs:
```bash
docker compose logs -f
```
