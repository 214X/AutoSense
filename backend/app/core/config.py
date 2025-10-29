from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    # app
    APP_NAME: str = os.getenv("APP_NAME")
    ENV: str = os.getenv("ENV")
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))

    # LLM / Ollama
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL")

settings = Settings()
