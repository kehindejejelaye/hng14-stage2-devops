# Stage 1: Build
FROM python:3.12-alpine3.20 as builder

WORKDIR /app

# Install build dependencies for some python packages if needed
RUN apk add --no-cache gcc musl-dev python3-dev

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.12-alpine3.20

WORKDIR /app

# Create a non-root user with home directory
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -h /home/appuser

# Copy installed packages from builder with correct ownership
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

COPY --chown=appuser:appuser main.py .

# Update PATH and set PYTHONUSERBASE so python finds the packages
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUSERBASE=/home/appuser/.local

USER appuser

EXPOSE 8000

# Using python -c for healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c 'import urllib.request; urllib.request.urlopen("http://localhost:8000/docs")' || exit 1

CMD ["python", "main.py"]
