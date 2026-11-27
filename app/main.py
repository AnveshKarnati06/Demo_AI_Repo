from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .agent import run_agent

# FastAPI Application
app = FastAPI(title="IT Service & Asset Operations Assistant",version="1.0.0")
STATIC_DIR = (Path(__file__).resolve().parent.parent/ "static")

# Request Schema
class ChatRequest(BaseModel):
    message: str = Field(min_length=2,max_length=1500)
    history: list[dict] = []

# Health Check
@app.get("/health")
def health():
    return {
        "status": "ok",
        "application":
            "IT Service & Asset Operations Assistant"
}

# Chat Endpoint
@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        return run_agent(
            request.message,
            request.history
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

# Home Page
@app.get("/")
def home():
    return FileResponse(
        STATIC_DIR / "index.html"
    )

# Static Files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)