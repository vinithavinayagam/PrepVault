import json
from pathlib import Path

from pypdf import PdfReader

INPUT_DIR = Path("data/incoming")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "tenant_extracted_pages.jsonl"


def extract_tenant_pdfs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(INPUT_DIR.rglob("*.pdf"))

    total_pages = 0
    successful_pages = 0
    failed_pages = 0

    print(f"Found {len(pdf_files)} tenant PDFs")

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for pdf_path in pdf_files:
            relative_path = pdf_path.relative_to(INPUT_DIR)

            college_slug = relative_path.parts[0]
            subject = relative_path.parts[1]

            print(f"\nCollege: {college_slug}")
            print(f"Subject: {subject}")
            print(f"PDF: {pdf_path.name}")

            try:
                reader = PdfReader(str(pdf_path))

                for page_number, page in enumerate(reader.pages, start=1):
                    total_pages += 1

                    try:
                        page_text = page.extract_text() or ""

                        if not page_text.strip():
                            continue

                        record = {
                            "college_slug": college_slug,
                            "subject": subject,
                            "source": pdf_path.name,
                            "source_path": relative_path.as_posix(),
                            "page": page_number,
                            "text": page_text.strip(),
                        }

                        output.write(json.dumps(record, ensure_ascii=False) + "\n")

                        successful_pages += 1

                    except Exception as error:
                        failed_pages += 1
                        print(f"Page error {page_number}: {error}")

                print(f"Completed: {len(reader.pages)} pages")

            except Exception as error:
                failed_pages += 1
                print(f"PDF error: {pdf_path.name}: {error}")

    print("\n========== TENANT EXTRACTION SUMMARY ==========")
    print(f"PDF files found: {len(pdf_files)}")
    print(f"Total pages attempted: {total_pages}")
    print(f"Successfully extracted pages: {successful_pages}")
    print(f"Failed pages: {failed_pages}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_tenant_pdfs()
