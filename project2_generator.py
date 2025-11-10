# project2_generator.py
import requests
import time
import random
from datetime import datetime

# The ingestion service runs on port 8000, 
# and from the generator's perspective, it's accessible at localhost:8000
INGESTION_URL = "http://localhost:8000/ingest/quote" 
SYMBOLS = ["AAPL", "GOOG", "MSFT", "AMZN"]
BASE_PRICE = {"AAPL": 170.0, "GOOG": 1500.0, "MSFT": 420.0, "AMZN": 180.0}

def generate_and_send_quote():
    """Generates a random quote and sends it to the Ingestion API."""
    symbol = random.choice(SYMBOLS)
    
    # Simulate random walk (price change)
    base = BASE_PRICE[symbol]
    price = round(base + random.uniform(-0.5, 0.5), 2)
    BASE_PRICE[symbol] = price # Update base for next iteration

    volume = random.randint(100, 1000)

    payload = {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(INGESTION_URL, json=payload)
        response.raise_for_status() # Raise exception for bad status codes
        print(f"Sent: {symbol} @ {price}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Ingestion API: {e}")

if __name__ == "__main__":
    # Ensure requests package is installed in your local environment to run this outside Docker
    # We will run this script locally to simulate an external feed hitting the Dockerized API
    
    print("Starting market data generator. Press Ctrl+C to stop.")
    while True:
        generate_and_send_quote()
        # High-frequency data: 20 updates per second
        time.sleep(0.05)