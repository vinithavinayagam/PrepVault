import json
from pathlib import Path

from pypdf import PdfReader

DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "extracted_pages.jsonl"


def extract_pdfs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    total_pages = 0
    successful_pages = 0
    failed_pages = 0

    print(f"Found {len(pdf_files)} PDF files")

    try:
        with OUTPUT_FILE.open("w", encoding="utf-8") as output:
            for pdf_path in pdf_files:
                print(f"\nProcessing: {pdf_path.name}")

                try:
                    reader = PdfReader(str(pdf_path))

                    for page_number, page in enumerate(reader.pages, start=1):
                        total_pages += 1

                        try:
                            text = page.extract_text() or ""

                            if text.strip():
                                record = {"source": pdf_path.name, "page": page_number, "text": text.strip()}

                                output.write(json.dumps(record, ensure_ascii=False) + "\n")
                                output.flush()
                                successful_pages += 1

                            else:
                                print(f"Empty page: {page_number}")

                        except Exception as error:
                            failed_pages += 1
                            print(f"Page error: {pdf_path.name}, page {page_number}: {error}")

                        if page_number % 25 == 0:
                            print(f"Progress: {page_number}/{len(reader.pages)} pages")

                    print(f"Completed: {pdf_path.name}")

                except Exception as error:
                    print(f"PDF error: {pdf_path.name}: {error}")

    except KeyboardInterrupt:
        print("\nExtraction interrupted.")
        print("Already extracted pages are saved.")

    print("\n========== EXTRACTION SUMMARY ==========")
    print(f"Total pages attempted: {total_pages}")
    print(f"Successfully extracted: {successful_pages}")
    print(f"Failed pages: {failed_pages}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_pdfs()
