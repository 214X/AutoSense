import requests
from typing import Iterable
from .llm_provider import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434"):
        self.url = f"{host}/api/generate"
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False} | kwargs
        r = requests.post(self.url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "")

    def stream(self, prompt: str, **kwargs) -> Iterable[str]:
        payload = {"model": self.model, "prompt": prompt, "stream": True} | kwargs
        with requests.post(self.url, json=payload, stream=True, timeout=0) as r:
            r.raise_for_status()
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    import json
                    chunk = json.loads(line)
                    yield chunk.get("response", "")
                except Exception:
                    continue
