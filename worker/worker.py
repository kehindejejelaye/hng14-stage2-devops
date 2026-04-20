import redis
import time
import os
import signal
import sys

# Environment configurations
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Signal handler for graceful shutdown
def shutdown_handler(signum, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    try:
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except redis.RedisError as e:
        print(f"Redis Error for {job_id}: {e}")

if __name__ == "__main__":
    print(f"Worker started, connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    while True:
        try:
            job = r.brpop("job", timeout=5)
            if job:
                _, job_id = job
                process_job(job_id.decode())
        except redis.ConnectionError:
            print("Redis connection lost. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(1)
