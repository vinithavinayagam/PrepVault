import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.database import SessionLocal
from app.models import Document, DocumentChunk

INPUT_FILE = Path("data/processed/tenant_chunks.jsonl")
BATCH_SIZE = 100


def import_chunks():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        records = [json.loads(line) for line in file if line.strip()]

    print(f"Loaded {len(records)} chunks")

    with SessionLocal.begin() as db:
        documents = db.execute(select(Document.id, Document.file_path)).all()

        document_ids = {file_path: document_id for document_id, file_path in documents}

        rows = []

        for record in records:
            source_path = record["source_path"]
            document_id = document_ids.get(source_path)

            if document_id is None:
                raise ValueError(f"Document not registered: {source_path}")

            rows.append(
                {
                    "document_id": document_id,
                    "page_number": record["page"],
                    "chunk_index": record["chunk_index"],
                    "chunk_text": record["text"],
                }
            )

        inserted = 0

        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start : start + BATCH_SIZE]

            statement = (
                insert(DocumentChunk)
                .values(batch)
                .on_conflict_do_nothing(constraint="uq_document_page_chunk")
            )

            result = db.execute(statement)
            inserted += result.rowcount

            print(f"Processed {min(start + BATCH_SIZE, len(rows))}/{len(rows)} chunks")

    print("\n========== IMPORT SUMMARY ==========")
    print(f"Chunks loaded: {len(records)}")
    print(f"New chunks inserted: {inserted}")
    print(f"Already existing: {len(records) - inserted}")


if __name__ == "__main__":
    import_chunks()
