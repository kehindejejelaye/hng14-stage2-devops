# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY main.py .

# Update PATH
ENV PATH=/home/appuser/.local/bin:$PATH

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Using python -c for healthcheck because curl is not installed in slim
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c 'import urllib.request; urllib.request.urlopen("http://localhost:8000/docs")' || exit 1

CMD ["python", "main.py"]
