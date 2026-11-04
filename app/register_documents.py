from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import College, Course, Document

INPUT_DIR = Path("data/incoming")


def register_documents():
    pdf_files = sorted(INPUT_DIR.rglob("*.pdf"))

    print(f"Found {len(pdf_files)} PDFs")

    with SessionLocal() as db:
        try:
            for pdf_path in pdf_files:
                relative_path = pdf_path.relative_to(INPUT_DIR)
                college_slug = relative_path.parts[0]
                subject = relative_path.parts[1]
                file_path = relative_path.as_posix()

                college = db.scalar(select(College).where(College.slug == college_slug))

                if college is None:
                    raise ValueError(f"College not found: {college_slug}")

                course_name = subject.replace("_", " ")

                course = db.scalar(
                    select(Course).where(
                        Course.college_id == college.id,
                        Course.name == course_name,
                        Course.batch == "2027",
                    )
                )

                if course is None:
                    raise ValueError(f"Course not found: {college_slug}/{course_name}")

                document = db.scalar(select(Document).where(Document.file_path == file_path))

                if document is None:
                    document = Document(
                        course_id=course.id,
                        filename=pdf_path.name,
                        file_path=file_path,
                    )
                    db.add(document)
                    print(f"Registered: {college_slug}/{subject}/{pdf_path.name}")
                elif document.course_id != course.id:
                    raise ValueError(f"Document is linked to the wrong course: {file_path}")
                else:
                    print(f"Already registered: {file_path}")

            db.commit()
            print("\nPDF registration completed.")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    register_documents()
