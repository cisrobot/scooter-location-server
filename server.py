from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import HTMLResponse
from pathlib import Path
import re

app = FastAPI()
scooter_locations: Dict[int, Dict] = {}

class ScooterData(BaseModel):
    data: str  # 예: "count: 1 / (ID: 0, lat: ..., lon: ...)"

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
