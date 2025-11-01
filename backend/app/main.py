from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

#router imports
from .api.chat_router import router as chat_router


load_dotenv()
app = FastAPI(title="AutoSense API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

def cli():
    """poetry run autosense-api"""
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

# include routers
app.include_router(chat_router)
