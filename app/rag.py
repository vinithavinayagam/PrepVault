from google import genai
from google.genai import types
from sqlalchemy import select

from app.config import get_settings
from app.database import SessionLocal
from app.models import College, Course, Document, DocumentChunk

EMBEDDING_MODEL = "gemini-embedding-2"
DIMENSIONS = 768
TOP_K = 5


def embed_question(question: str) -> list[float]:
    settings = get_settings()

    client = genai.Client(api_key=settings.gemini_api_key)

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question,
        config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS),
    )

    if not response.embeddings:
        raise RuntimeError("Question embedding was not generated")

    return response.embeddings[0].values


def retrieve_chunks(question: str, college_slug: str) -> list[dict]:
    query_vector = embed_question(question)

    statement = (
        select(
            DocumentChunk.chunk_text,
            DocumentChunk.page_number,
            Document.filename,
            DocumentChunk.embedding.cosine_distance(query_vector).label("distance"),
        )
        .join(Document, DocumentChunk.document_id == Document.id)
        .join(Course, Document.course_id == Course.id)
        .join(College, Course.college_id == College.id)
        .where(
            College.slug == college_slug,
            DocumentChunk.embedding.is_not(None),
        )
        .order_by("distance")
        .limit(TOP_K)
    )

    with SessionLocal() as db:
        results = db.execute(statement).all()

    return [
        {
            "text": row.chunk_text,
            "filename": row.filename,
            "page": row.page_number,
            "distance": float(row.distance),
        }
        for row in results
    ]


def generate_rag_answer(question: str, college_slug: str) -> dict:
    settings = get_settings()

    if not settings.gemini_api_key:
        raise ValueError("Gemini API key is missing")

    chunks = retrieve_chunks(question, college_slug)

    if not chunks:
        return {
            "answer": "I could not find relevant information in your college materials.",
            "citations": [],
        }

    context = "\n\n".join(
        f"Source: {chunk['filename']}, Page: {chunk['page']}\nContent: {chunk['text']}" for chunk in chunks
    )

    prompt = f"""
You are PrepVault, a college study assistant.

Answer the question using ONLY the provided college materials.
If the answer is not available in the materials, say:
"I could not find this information in your college materials."

Include page citations in this format: [filename, p. X].
Do not invent facts or citations.

Question: {question}

College materials:
{context}
"""

    client = genai.Client(api_key=settings.gemini_api_key)

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    citations = [
        {
            "filename": chunk["filename"],
            "page": chunk["page"],
        }
        for chunk in chunks
    ]

    return {
        "answer": response.text,
        "citations": citations,
    }
