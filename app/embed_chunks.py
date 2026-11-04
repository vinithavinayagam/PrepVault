import time

from google import genai
from google.genai import types
from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings
from app.database import SessionLocal
from app.models import DocumentChunk

MODEL = "gemini-embedding-2"
BATCH_SIZE = 10
DIMENSIONS = 768


settings = get_settings()

if not settings.gemini_api_key:
    raise ValueError("Gemini API key is missing")

client = genai.Client(api_key=settings.gemini_api_key)


@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=20),
    reraise=True,
)
def generate_embeddings(texts):
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=text)],
        )
        for text in texts
    ]

    response = client.models.embed_content(
        model=MODEL,
        contents=contents,
        config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS),
    )

    if len(response.embeddings) != len(texts):
        raise ValueError(f"Expected {len(texts)} embeddings, received {len(response.embeddings)}")

    return [item.values for item in response.embeddings]


def embed_pending_chunks():
    total_processed = 0

    with SessionLocal() as db:
        while True:
            chunks = db.scalars(
                select(DocumentChunk)
                .where(DocumentChunk.embedding.is_(None))
                .order_by(DocumentChunk.id)
                .limit(BATCH_SIZE)
            ).all()

            if not chunks:
                break

            try:
                texts = [chunk.chunk_text for chunk in chunks]
                vectors = generate_embeddings(texts)

                for chunk, vector in zip(chunks, vectors, strict=True):
                    if len(vector) != DIMENSIONS:
                        raise ValueError("Unexpected embedding dimension")

                    chunk.embedding = vector

                db.commit()
                total_processed += len(chunks)

                print(f"Embedded and saved: {total_processed} chunks")
                time.sleep(1.5)
                time.sleep(10)

            except Exception:
                db.rollback()
                raise

    print("\n========== EMBEDDING SUMMARY ==========")
    print(f"New embeddings saved: {total_processed}")


if __name__ == "__main__":
    embed_pending_chunks()
