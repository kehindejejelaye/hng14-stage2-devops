# BUG FIXES

| File | Line | Problem | Fix |
|---|---|---|---|
| `api/main.py` | 9 | Hardcoded Redis host `localhost` | Use `os.getenv("REDIS_HOST", "localhost")` for dynamic configuration |
| `api/main.py` | 9 | Hardcoded Redis port `6379` | Use `int(os.getenv("REDIS_PORT", 6379))` for dynamic configuration |
| `worker/worker.py` | 6 | Hardcoded Redis host `localhost` | Use `os.getenv("REDIS_HOST", "localhost")` for dynamic configuration |
| `worker/worker.py` | 6 | Hardcoded Redis port `6379` | Use `int(os.getenv("REDIS_PORT", 6379))` for dynamic configuration |
| `frontend/app.js` | 6 | Hardcoded `API_URL` `http://localhost:8000` | Use `process.env.API_HOST \|\| "localhost"` and `process.env.API_PORT \|\| 8000` to construct the URL dynamically |
| `frontend/app.js` | 24 | Hardcoded port `3000` | Use `process.env.PORT \|\| 3000` |
| `api/main.py` | 20 | Potential `NoneType` decode error if `status` is None | Added check if `status` exists before decoding |
| `worker/worker.py` | 14 | Missing error handling and graceful shutdown | Implement `signal` handlers for `SIGTERM` and `SIGINT` |
| `api/main.py` | N/A | Missing `uvicorn` startup entry point | Added `if __name__ == "__main__":` block to run with uvicorn |
| `api/main.py` | 13 | Redis `lpush` followed by `hset` can lead to race conditions where worker pops before status is set | Reordered: `hset` before `lpush` |
| `frontend/app.js` | 33 | Redundant and brittle log statement using full URL | Refactor to log host and port separately for clarity and accuracy |
| `api/Dockerfile` | N/A | Running as root and missing healthcheck | Implemented multi-stage build, non-root user `appuser`, and added `HEALTHCHECK` |
| `worker/Dockerfile` | N/A | Running as root, missing healthcheck, and missing `procps` | Implemented multi-stage build, non-root user `appuser`, installed `procps`, and added `HEALTHCHECK` |
| `frontend/Dockerfile` | N/A | Running as root and missing healthcheck | Implemented multi-stage build, non-root user `appuser`, and added `HEALTHCHECK` |
| `docker-compose.yml` | N/A | Missing resource limits, health-dependent startup, and dynamic configuration | Added CPU/Memory limits, `condition: service_healthy` for `depends_on`, and configured via environment variables |
| `N/A` | N/A | Missing automated testing and CI/CD pipeline | Implemented full GitHub Actions pipeline with Lint, Test, Build, Security Scan, Integration Test, and Deploy stages `.github/workflows/pipeline.yml` |
| `N/A` | N/A | Missing scripted rolling update deployment | Created `deploy.sh` script to perform zero-downtime rolling updates with health validation |
| `api/test_main.py` | 14 | `ModuleNotFoundError: No module named 'api'` during test execution | Explicitly add parent directory to `sys.path` to ensure module resolution |
| `docker-compose.yml` | N/A | Hardcoded service configurations and missing environment variable overrides | Replaced hardcoded values with `${VAR:-default}` syntax for all service environments and ports |
| `api/Dockerfile` | 17,21 | Missing home directory for `appuser` and incorrect package ownership | Used `useradd -m`, `COPY --chown`, and set `PYTHONUSERBASE` for correct non-root execution |
| `worker/Dockerfile` | 14,18 | Missing home directory for `appuser` and incorrect package ownership | Used `useradd -m`, `COPY --chown`, and set `PYTHONUSERBASE` for correct non-root execution |
| `deploy.sh` | 13 | Renaming fails if a stopped container with the same name exists | Changed `docker ps` to `docker ps -a` with exact name filtering to handle stopped containers |
| `deploy.sh` | 24 | New containers start without environment variables, causing potential failures | Added logic to automatically use `.env` file via `--env-file` if present |
| `N/A` | N/A | Missing `.dockerignore` files | Created `.dockerignore` for each service to exclude `.env`, `.git`, and `__pycache__` |
| `pytest.ini` | N/A | Missing pytest configuration for discovery | Created `pytest.ini` at root to standardize test discovery and pythonpath |
