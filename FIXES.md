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
