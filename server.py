from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# 루트 경로 확인용
@app.get("/")
def root():
    return {"message": "Server is running"}

# 데이터 형식을 정의 (ROS2에서 보내는 메시지 구조와 맞춰야 함)
class ScooterData(BaseModel):
    data: str  # 예: "count: 3 / (ID: 1, lat: ..., lon: ...), ..."

# POST 요청 처리 경로
@app.post("/api/scooters")
async def receive_scooter_data(payload: ScooterData):
    print("[SERVER] Received:", payload.data)
    # 여기서 DB 저장, 로그 기록, 알림 전송 등 가능
    return {"status": "received"}

