from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any, Optional

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        ...

    @abstractmethod
    def stream(self, prompt: str, **kwargs) -> Iterable[str]:
        ...