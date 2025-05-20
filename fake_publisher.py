import requests
import random
import time

SERVER_URL = "https://scooter-location-server.onrender.com/api/scooters"

def generate_fake_data():
    count = random.randint(1, 3)
    data_str = f"count: {count} / "
    for i in range(count):
        lat = round(36.123456 + random.uniform(-0.001, 0.001), 6)
        lon = round(128.654321 + random.uniform(-0.001, 0.001), 6)
        data_str += f"(ID: {i}, lat: {lat}, lon: {lon}), "
    return data_str.strip(", ")

def main():
    while True:
        fake_data = generate_fake_data()
        print("[SIM] Sending:", fake_data)
        try:
            response = requests.post(SERVER_URL, json={"data": fake_data})
            print(f"[SIM] Response: {response.status_code}")
        except Exception as e:
            print(f"[SIM] Error: {e}")
        time.sleep(3)

if __name__ == "__main__":
    main()
