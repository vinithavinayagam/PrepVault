import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.config import Settings, get_settings
from app.database import initialize_database
from app.llm import generate_answer
from app.schemas import ChatRequest, ChatResponse
from app.usage import (
    get_usage as read_usage,
)
from app.usage import (
    initialize_usage_db,
    record_usage,
)

app = FastAPI(title="Examate RAG starter", version="0.1.0")
logger = logging.getLogger(__name__)

SettingsDep = Annotated[Settings, Depends(get_settings)]

initialize_usage_db()
initialize_database()


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        answer = generate_answer(request.question)
        record_usage("success")

        return ChatResponse(
            question=request.question,
            answer=answer,
            status="success",
        )

    except Exception as exc:
        logger.exception("Gemini chat request failed")
        record_usage("failed")

        raise HTTPException(
            status_code=502,
            detail="LLM service failed. Please try again.",
        ) from exc


@app.get("/usage")
def usage() -> dict:
    return read_usage()