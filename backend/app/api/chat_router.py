from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Literal
from datetime import datetime
from fastapi.responses import StreamingResponse
from typing import Iterator
import requests


from ..core.config import settings
from ..providers.ollama_provider import OllamaProvider

# ROUTER
router = APIRouter(prefix="/api/chat", tags=["chat"])

# CONSTANTS
MAX_HISTORY_TURNS = 5
SYSTEM_PROMPT = (
    "Just keep the conversation."
)

# TYPES
Role = Literal["assistant", "user"]

# MODELS
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)

class Message(BaseModel):
    role: Role
    content: str
    timestamp: str  # ISO-8601 UTC

class ChatResponse(BaseModel):
    reply: Message
    history_len: int

# LLM PROVIDER
provider = OllamaProvider(
    model=settings.OLLAMA_MODEL,
    host=settings.OLLAMA_HOST,
)

# CHAT STORE CLASS
class ChatStore:
    """This class keeps the chat history."""
    def __init__(self) -> None:
        # [{"role": "...", "content": "...", "timestamp": "..."}]
        self.history: List[Dict[str, str]] = []

    def append(self, role: Role, content: str) -> str:
        ts = datetime.utcnow().isoformat()
        self.history.append({"role": role, "content": content, "timestamp": ts})
        return ts

    def get_length(self) -> int:
        return len(self.history)

    def clear(self) -> None:
        self.history.clear()

    def get_chat_history(self, turns: int) -> List[Dict[str, str]]:
        max_msgs = 2 * turns
        if len(self.history) > max_msgs:
            return self.history[-max_msgs:]
        return self.history

chat_store = ChatStore()

# UTILS
def build_prompt(store: ChatStore, user_msg: str, max_history_turns: int) -> str:
    lines = [f"System: {SYSTEM_PROMPT}", ""]
    context_history = store.get_chat_history(max_history_turns)
    for turn in context_history:
        lines.append(f"{turn['role'].capitalize()}: {turn['content']}")
    lines.append(f"User: {user_msg}")
    lines.append("Assistant:")  # modelin cevabı için doğal tamamlayıcı
    return "\n".join(lines)

# ENDPOINTS
@router.get("/ping")
def ping():
    return {"ok": True, "scope": "chat", "msg": "pong"}

@router.post("/send", response_model=ChatResponse)
def send(req: ChatRequest):
    prompt = build_prompt(chat_store, req.message, MAX_HISTORY_TURNS)
    try:
        answer = provider.generate(prompt)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ollama connection error: {e}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    # store the user message
    chat_store.append("user", req.message)
    # store the modal response
    ts_assistant = chat_store.append("assistant", answer)

    return ChatResponse(
        reply=Message(role="assistant", content=answer, timestamp=ts_assistant),
        history_len=chat_store.get_length(),
    )

@router.post("/reset")
def reset():
    chat_store.clear()
    return {"ok": True, "history_len": 0}

@router.post("/stream")
def stream(req: ChatRequest):
    accumulator: list[str] = []

    def event_source() -> Iterator[bytes]:
        try:
            prompt = build_prompt(chat_store, req.message, MAX_HISTORY_TURNS)
            for chunk in provider.stream(prompt):
                text = str(chunk)
                accumulator.append(text)
                yield f"data: {text}\n\n".encode("utf-8")
        except requests.exceptions.RequestException as e:
            yield f"event: error\ndata: Ollama connection error: {e}\n\n".encode("utf-8")
        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n".encode("utf-8")
        else: # stream completed successfully
            chat_store.append("user", req.message)
            chat_store.append("assistant", "".join(accumulator))

    return StreamingResponse(event_source(), media_type="text/event-stream")

