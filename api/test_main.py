import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import os

# Set environment variables for testing
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"

# Mock redis before importing app to avoid connection errors during import
with patch("redis.Redis") as mock_redis_class:
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis
    from api.main import app

client = TestClient(app)


@pytest.fixture
def mock_r():
    with patch("api.main.r") as m:
        yield m


def test_create_job(mock_r):
    # Setup mock behavior
    mock_r.hset.return_value = 1
    mock_r.lpush.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert mock_r.hset.called
    assert mock_r.lpush.called


def test_get_job_status_completed(mock_r):
    job_id = "test-job-123"
    mock_r.hget.return_value = b"completed"

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json() == {"job_id": job_id, "status": "completed"}
    mock_r.hget.assert_called_with(f"job:{job_id}", "status")


def test_get_job_status_not_found(mock_r):
    job_id = "non-existent"
    mock_r.hget.return_value = None

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json() == {"error": "not found"}
    mock_r.hget.assert_called_with(f"job:{job_id}", "status")
