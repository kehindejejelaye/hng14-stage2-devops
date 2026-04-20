#!/bin/bash
set -e

# Usage: ./deploy.sh <service_name> <image_tag>
SERVICE_NAME=$1
IMAGE_TAG=$2

if [ -z "$SERVICE_NAME" ] || [ -z "$IMAGE_TAG" ]; then
    echo "Usage: ./deploy.sh <service_name> <image_tag>"
    exit 1
fi

OLD_CONTAINER=$(docker ps -f "name=${SERVICE_NAME}" --format "{{.ID}}" | head -n 1)
NEW_CONTAINER_NAME="${SERVICE_NAME}_new_$(date +%s)"

echo "Starting new container for ${SERVICE_NAME} with tag ${IMAGE_TAG}..."

# Construct environment variables if any are needed for healthcheck
# This assumes the network 'internal' exists from docker-compose
docker run -d \
  --name "${NEW_CONTAINER_NAME}" \
  --network hng14-stage2-devops_internal \
  "${IMAGE_TAG}"

# Wait for health check (max 60 seconds)
echo "Waiting for health check..."
COUNT=0
MAX_RETRIES=12
SLEEP_INTERVAL=5

HEALTHY=false
while [ $COUNT -lt $MAX_RETRIES ]; do
    STATUS=$(docker inspect --format='{{json .State.Health.Status}}' "${NEW_CONTAINER_NAME}" | tr -d '"')
    if [ "$STATUS" == "healthy" ]; then
        echo "New container is healthy!"
        HEALTHY=true
        break
    fi
    echo "Current status: ${STATUS:-starting}... waiting..."
    COUNT=$((COUNT+1))
    sleep $SLEEP_INTERVAL
done

if [ "$HEALTHY" = true ]; then
    echo "Replacing old container..."
    if [ ! -z "$OLD_CONTAINER" ]; then
        docker stop "$OLD_CONTAINER"
        docker rm "$OLD_CONTAINER"
    fi
    docker rename "${NEW_CONTAINER_NAME}" "${SERVICE_NAME}"
    echo "Deployment successful!"
else
    echo "New container failed health check. Aborting deployment."
    docker stop "${NEW_CONTAINER_NAME}"
    docker rm "${NEW_CONTAINER_NAME}"
    exit 1
fi
