from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4
import time

Role = str  # "system" | "user" | "assistant"

@dataclass
class Message:
    role: Role
    content: str
    ts: float = field(default_factory=lambda: time.time())

@dataclass
class Conversation:
    id: str
    messages: List[Message] = field(default_factory=list)

class ConversationStore:
    """
    In-memory conversation store.
    When the server restarts, all conversations are naturally cleared.
    """
    def __init__(self) -> None:
        self._store: Dict[str, Conversation] = {}

    def start(self, system_prompt: str | None = None) -> Conversation:
        """
        Create a new conversation and optionally include a system message.
        Returns the created Conversation object.
        """
        cid = str(uuid4())
        convo = Conversation(id=cid)
        if system_prompt:
            convo.messages.append(Message(role="system", content=system_prompt))
        self._store[cid] = convo
        return convo

    def get(self, cid: str) -> Conversation:
        """
        Retrieve an existing conversation by its ID.
        Raises KeyError if the conversation does not exist.
        """
        if cid not in self._store:
            raise KeyError(f"conversation not found: {cid}")
        return self._store[cid]

    def append(self, cid: str, role: Role, content: str) -> None:
        self.get(cid).messages.append(Message(role=role, content=content))

    def summarize_context(self, cid: str, max_chars: int = 6000) -> List[Message]:
        """
        Return the most recent messages within a simple character limit.
        Collects messages from the end backward until the limit is reached.
        """
        msgs = self.get(cid).messages
        acc: List[Message] = []
        total = 0
        for m in reversed(msgs):
            length = len(m.content) + 16
            if total + length > max_chars and acc:
                break
            acc.append(m)
            total += length
        return list(reversed(acc))

    def reset(self, cid: str) -> None:
        """
        Reset a specific conversation by ID.
        Raises KeyError if the conversation does not exist.
        """
        if cid not in self._store:
            raise KeyError(f"conversation not found: {cid}")
        self._store[cid] = Conversation(id=cid)

    def reset_all(self) -> None:
        self._store.clear()
