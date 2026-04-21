# Stage 1: Build
FROM python:3.12-alpine3.20 as builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.12-alpine3.20

WORKDIR /app

# Install procps for healthcheck if needed, but ps is in busybox
# and create a non-root user with home
RUN apk add --no-cache procps && \
    addgroup -S appgroup && adduser -S appuser -G appgroup -h /home/appuser

# Copy installed packages from builder with correct ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

COPY --chown=appuser:appuser worker.py .

# Update PATH and set PYTHONUSERBASE so python finds the packages
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUSERBASE=/home/appuser/.local

USER appuser

# Healthcheck for worker: check if process is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ps aux | grep "python worker.py" | grep -v grep || exit 1

CMD ["python", "worker.py"]
