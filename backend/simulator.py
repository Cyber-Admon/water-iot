"""
Simple simulator that sends fake sensor readings straight to the backend,
without needing an ESP32 at all. Useful for testing the API and dashboard
before hardware exists, or while the ESP32 firmware is still being wired up.

Usage:
    python simulator.py
"""
import random
import time
import requests

SERVER_URL = "http://localhost:8000/api/readings"
NODE_ID = "node-01"
SEND_INTERVAL_SECONDS = 10  # shorter than 60s for faster local testing


def generate_reading():
    return {
        "node_id": NODE_ID,
        "turbidity_ntu": round(random.uniform(0, 8), 2),
        "ph": round(random.uniform(6.0, 9.5), 2),
        "tds_ppm": round(random.uniform(0, 1200), 2),
        "temperature_c": round(random.uniform(24, 30), 2),
        "is_simulated": True,
    }


def main():
    print(f"Sending simulated readings to {SERVER_URL} every {SEND_INTERVAL_SECONDS}s. Ctrl+C to stop.")
    while True:
        reading = generate_reading()
        try:
            response = requests.post(SERVER_URL, json=reading, timeout=5)
            print(f"Sent: {reading} -> Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Could not connect to backend. Is it running? (docker compose up)")
        time.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
