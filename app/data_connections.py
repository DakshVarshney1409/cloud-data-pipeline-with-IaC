# app/data_connections.py
import redis
import os
from pymongo import MongoClient
from pymongo.collection import Collection

# --- Redis Setup (High-Speed Cache) ---
# Use the environment variables set in docker-compose
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialize the Redis connection pool
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_redis_client() -> redis.Redis:
    """Dependency to get the Redis client."""
    return redis_client

# --- MongoDB Setup (Time-Series Persistence) ---
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_USER = os.getenv("MONGO_USER", "mongo_user")
MONGO_PASS = os.getenv("MONGO_PASS", "mongo_pass")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/"

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.market_data_db
trades_collection: Collection = db.historical_quotes

def get_mongo_collection() -> Collection:
    """Dependency to get the MongoDB collection."""
    return trades_collection