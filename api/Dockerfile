# Stage 1: Build
FROM python:3.11-slim-bookworm as builder

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim-bookworm

WORKDIR /app

# Upgrade OS packages to resolve vulnerabilities
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Create a non-root user with home directory
RUN groupadd -r appuser && useradd -m -r -g appuser appuser

# Copy installed packages from builder with correct ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

COPY --chown=appuser:appuser main.py .

# Update PATH and set PYTHONUSERBASE so python finds the packages
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUSERBASE=/home/appuser/.local

USER appuser

EXPOSE 8000

# Using python -c for healthcheck because curl is not installed in slim
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c 'import urllib.request; urllib.request.urlopen("http://localhost:8000/docs")' || exit 1

CMD ["python", "main.py"]
