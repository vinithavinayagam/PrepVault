import json
from pathlib import Path

INPUT_FILE = Path("data/processed/extracted_pages.jsonl")
OUTPUT_FILE = Path("data/processed/chunks.jsonl")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def split_text(text):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))

        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start + CHUNK_SIZE // 2:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(start + 1, end - CHUNK_OVERLAP)

    return chunks


def create_chunks():
    total_chunks = 0

    with INPUT_FILE.open("r", encoding="utf-8") as source, OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for line_number, line in enumerate(source, start=1):
            page = json.loads(line)

            text_chunks = split_text(page["text"])

            for index, chunk in enumerate(text_chunks, start=1):
                record = {"source": page["source"], "page": page["page"], "chunk_index": index, "text": chunk}

                output.write(json.dumps(record, ensure_ascii=False) + "\n")

                total_chunks += 1

            if line_number % 100 == 0:
                print(f"Processed {line_number} pages")

    print("\n========== CHUNKING SUMMARY ==========")
    print(f"Total pages processed: {line_number}")
    print(f"Total chunks created: {total_chunks}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_chunks()
