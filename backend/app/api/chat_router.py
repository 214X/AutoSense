from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags = ["chat"])

@router.get("/ping")
def ping():
    return {"ok": True, "scope": "chat", "msg": "pong"}