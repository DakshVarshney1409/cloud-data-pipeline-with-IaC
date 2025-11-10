# app/ingestion_main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
import json

from .data_connections import get_redis_client, get_mongo_collection
from redis import Redis
from pymongo.collection import Collection

app = FastAPI()

# Pydantic Model for incoming data payload
class Quote(BaseModel):
    symbol: str
    price: float
    volume: int
    timestamp: datetime

from time import sleep

# Add a startup event hook to wait for and confirm database readiness
@app.on_event("startup")
def resilient_startup():
    """Waits for Redis and MongoDB to be available before proceeding."""
    redis_client = get_redis_client()
    
    # 1. Wait for Redis
    max_retries = 10
    for i in range(max_retries):
        try:
            redis_client.ping()
            print("Redis is available.")
            break
        except Exception:
            print(f"Waiting for Redis... Retry {i+1}/{max_retries}")
            sleep(2)
    else:
        # If the loop completes without breaking, Redis failed to connect
        raise ConnectionError("FATAL: Could not connect to Redis after multiple retries.")

# --- Endpoint 1: High-Throughput Ingestion API ---
@app.post("/ingest/quote", status_code=202)
def ingest_market_quote(
    quote: Quote,
    redis_client: Redis = Depends(get_redis_client),
    mongo_collection: Collection = Depends(get_mongo_collection)
):
    """Receives a single market quote, caches the price, and persists the record."""
    
    # 1. Update Real-Time Cache (Low-latency)
    # Cache key: "last_price:{SYMBOL}"
    redis_client.set(f"last_price:{quote.symbol}", quote.price)
    
    # Cache the entire quote for API retrieval (optional, but useful)
    redis_client.set(f"last_quote:{quote.symbol}", quote.model_dump_json())

    # 2. Persist to NoSQL Database (High-throughput)
    # MongoDB is excellent for high volume time-series data
    try:
        mongo_collection.insert_one(quote.model_dump(by_alias=True))
    except Exception as e:
        print(f"MongoDB write failed: {e}")
        # In a real system, we'd log this and push to a dead-letter queue
        
    return {"status": "accepted", "symbol": quote.symbol}


# --- Endpoint 2: Low-Latency Cache Retrieval API ---
@app.get("/market_data/last_price/{symbol}")
def get_last_price(
    symbol: str,
    redis_client: Redis = Depends(get_redis_client)
):
    """Fetches the latest price directly from the Redis cache (low latency)."""
    price = redis_client.get(f"last_price:{symbol}")
    if price is None:
        raise HTTPException(status_code=404, detail="Symbol not found in cache")
    
    return {"symbol": symbol, "price": float(price)}

# --- Optional: Check connection status ---
@app.get("/health")
def health_check(
    redis_client: Redis = Depends(get_redis_client),
    mongo_collection: Collection = Depends(get_mongo_collection)
):
    """Verifies connections to Redis and MongoDB."""
    redis_status = redis_client.ping()
    mongo_status = mongo_client.admin.command('ping')['ok'] == 1.0

    return {
        "redis_status": "OK" if redis_status else "FAIL",
        "mongodb_status": "OK" if mongo_status else "FAIL"
    }