from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Literal
from datetime import datetime
import requests

from ..core.config import settings
from ..providers.ollama_provider import OllamaProvider

router = APIRouter(prefix="/api/chat", tags = ["chat"])

# to keep the all messages
HISTORY: List[Dict[str, str]] = []

# to distinguish the message sender
Role = Literal["assistant", "user"]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)

class Message(BaseModel):
    role: Role
    content: str
    timestamp: str

class ChatResponse(BaseModel):
    reply: Message
    history_len: int

provider = OllamaProvider(
    model=settings.OLLAMA_MODEL,
    host=settings.OLLAMA_HOST,
)

SYSTEM_PROMPT = (
    "System role: No role. Just keep the conversation going."
    "Input information: Dialouge history will be given you."
)

MAX_HISTORY_TURNS = 5

def get_context_history(history: List[Dict(str, str)], max_turns):
    max_msgs = 2 * max_turns
    return history[-max_msgs:] if (len(history) > max_msgs) else history

def build_prompt(history: List[Dict[str, str]], user_msg: str, max_history_turns: int):
    lines = [f"Systeme: {SYSTEM_PROMPT}", ""]
    context_history = get_context_history(history, max_history_turns)
    for turn in context_history:
        lines.append(f"{turn['role'].capitalize()}: {turn['content']}")
    lines.append(f"User: {user_msg}")
    return "\n".join(lines)


# ENDPOINTS
@router.get("/ping")
def ping():
    return {"ok": True, "scope": "chat", "msg": "pong"}

@router.post("/send", response_model=ChatResponse)
def send(req: ChatRequest):
    prompt = build_prompt(HISTORY, req.message, MAX_HISTORY_TURNS)
    try:
        answer = provider.generate(prompt)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ollama connection error: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    now = datetime.utcnow().isoformat()

    HISTORY.append({"role": "user", "content": req.message, "timestamp": now})
    HISTORY.append({"role": "assistant", "content": answer, "timestamp": datetime.utcnow().isoformat()})

    return ChatResponse(
        reply=Message(role="assistant", content=answer, timestamp=now),
        history_len=len(HISTORY),
    )

@router.post("/reset")
def reset():
    HISTORY.clear()
    return {"ok": True, "history_len": 0}
