from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ScooterMessage(BaseModel):
    data: str

scooter_log = []

@app.post("/api/scooters")
async def receive_data(msg: ScooterMessage):
    scooter_log.append(msg.data)
    print(f"[SERVER] Received: {msg.data}")
    return {"status": "ok"}
