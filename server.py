from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import re

app = FastAPI()
scooter_locations: Dict[int, Dict] = {}

class ScooterData(BaseModel):
    data: str  # 예: "count: 2 / (ID: 1, lat: 36.654321, lon: 128.654321)"

@app.post("/api/scooters")
def receive_data(payload: ScooterData):
    print("[SERVER] Received:", payload.data)

    # 정규표현식으로 여러 킥보드 ID, 위도, 경도 추출
    matches = re.findall(r"ID: (\d+), lat: ([\d.]+), lon: ([\d.]+)", payload.data)
    for id_str, lat, lon in matches:
        id_int = int(id_str)
        scooter_locations[id_int] = {
            "id": id_int,
            "lat": float(lat),
            "lon": float(lon)
        }

    return {"status": "ok"}

@app.get("/api/scooters")
def get_all_data():
    return {"scooters": list(scooter_locations.values())}

@app.get("/")
def root():
    return {"message": "Server is running"}

