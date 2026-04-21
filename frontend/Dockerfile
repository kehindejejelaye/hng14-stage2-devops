# Stage 1: Build
FROM node:18-alpine3.20 AS builder

WORKDIR /app

COPY package.json .
RUN npm install --omit=dev

# Stage 2: Production
FROM node:18-alpine3.20

WORKDIR /app

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy installed packages and code from builder
COPY --from=builder /app/node_modules ./node_modules
COPY app.js .
COPY views ./views

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

# Healthcheck for frontend: check if server is listening
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (res) => res.statusCode === 200 ? process.exit(0) : process.exit(1))" || exit 1

CMD ["node", "app.js"]
