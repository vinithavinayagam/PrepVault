import json
from pathlib import Path

from chunking import split_text

INPUT_FILE = Path("data/processed/tenant_extracted_pages.jsonl")
OUTPUT_FILE = Path("data/processed/tenant_chunks.jsonl")


def create_tenant_chunks():
    total_chunks = 0
    total_pages = 0

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with INPUT_FILE.open("r", encoding="utf-8") as source, OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for line_number, line in enumerate(source, start=1):
            page = json.loads(line)
            total_pages += 1

            for index, chunk in enumerate(split_text(page["text"]), start=1):
                record = {
                    "college_slug": page["college_slug"],
                    "subject": page["subject"],
                    "source": page["source"],
                    "source_path": page["source_path"],
                    "page": page["page"],
                    "chunk_index": index,
                    "text": chunk,
                }

                output.write(json.dumps(record, ensure_ascii=False) + "\n")

                total_chunks += 1

            if line_number % 100 == 0:
                print(f"Processed {line_number} pages")

    print("\n========== TENANT CHUNKING SUMMARY ==========")
    print(f"Pages processed: {total_pages}")
    print(f"Total chunks created: {total_chunks}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_tenant_chunks()
