from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import HTMLResponse
from pathlib import Path
import re
import requests

app = FastAPI()
scooter_locations: Dict[int, Dict] = {}

class ScooterData(BaseModel):
    data: str  # 예: "count: 1 / (ID: 0, lat: ..., lon: ...)"

def send_telegram_alert(scooter_id, lat, lon):
    BOT_TOKEN = "7666971770:AAEcgpNd7NHLXrU4PKi3Z6qKA0aJhECDZE0"
    CHAT_ID = "8002468150"
    map_url = f"https://www.google.com/maps?q={lat},{lon}"
    message = f"🛴 킥보드 탐지!\nID: {scooter_id}\n📍 지도 보기: {map_url}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
        print(f"[Telegram] Status: {r.status_code}, Response: {r.text}")  # ✅ 로그 추가
    except Exception as e:
        print(f"[Telegram Error] {e}")

@app.post("/api/scooters")
def receive_data(payload: ScooterData):
    print("[SERVER] Received:", payload.data)
    matches = re.findall(r"ID: (\d+), lat: ([\d.]+), lon: ([\d.]+)", payload.data)
    for id_str, lat, lon in matches:
        id_int = int(id_str)
        scooter_locations[id_int] = {
            "id": id_int,
            "lat": float(lat),
            "lon": float(lon),
            "map_url": f"https://www.google.com/maps?q={lat},{lon}"
        }

        print(f"[DEBUG] Calling Telegram alert for ID: {id_int}")  # ✅ 로그 추가
        send_telegram_alert(id_int, lat, lon)

    return {"status": "ok"}

@app.get("/api/scooters")
def get_all_data():
    return {"scooters": list(scooter_locations.values())}

@app.get("/")
def root():
    return {"message": "Server is running"}

@app.get("/map", response_class=HTMLResponse)
def get_map():
    html_path = Path(__file__).parent / "map.html"
    return HTMLResponse(content=html_path.read_text(), status_code=200)
