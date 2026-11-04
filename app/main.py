import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text

from app.config import Settings, get_settings
from app.database import engine, initialize_database
from app.llm import generate_answer
from app.rag import generate_rag_answer
from app.schemas import (
    AskRequest,
    AskResponse,
    ChatRequest,
    ChatResponse,
)
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


@app.get("/ready")
def ready() -> dict:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as exc:
        logger.exception("Readiness check failed")
        raise HTTPException(
            status_code=503,
            detail="Database is not ready",
        ) from exc


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


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        result = generate_rag_answer(
            request.question,
            request.college_slug,
        )

        record_usage("success")

        return AskResponse(
            question=request.question,
            college_slug=request.college_slug,
            answer=result["answer"],
            citations=result["citations"],
            status="success",
        )

    except Exception as exc:
        logger.exception("RAG request failed")
        record_usage("failed")

        raise HTTPException(
            status_code=502,
            detail="RAG service failed. Please try again.",
        ) from exc
