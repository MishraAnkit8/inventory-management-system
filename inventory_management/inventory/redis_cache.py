# redis_cache.py
import redis
from django.conf import settings

# Initialize Redis connection
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=0, 
    decode_responses=True
)

def redis_connect():
    """Test Redis connection"""
    try:
        redis_client.ping()
        print("Redis is connected successfully.")
    except redis.ConnectionError:
        print("Failed to connect to Redis.")
