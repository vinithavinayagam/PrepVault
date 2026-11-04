from sqlalchemy import select

from app.database import SessionLocal
from app.models import College, Course

TENANTS = [
    {
        "name": "Demo College",
        "slug": "demo_college",
        "courses": ["DSA", "Python", "System Design"],
    },
    {
        "name": "Prince Shri Venkateshwara Padmavathy Engineering College",
        "slug": "psvpec",
        "courses": ["DSA", "DBMS"],
    },
]

BATCH = "2027"


def register_tenants():
    with SessionLocal() as db:
        try:
            for tenant in TENANTS:
                college = db.scalar(select(College).where(College.slug == tenant["slug"]))

                if college is None:
                    college = College(
                        name=tenant["name"],
                        slug=tenant["slug"],
                    )
                    db.add(college)
                    db.flush()
                    print(f"Created college: {tenant['slug']}")
                else:
                    print(f"College already exists: {tenant['slug']}")

                for course_name in tenant["courses"]:
                    course = db.scalar(
                        select(Course).where(
                            Course.college_id == college.id,
                            Course.name == course_name,
                            Course.batch == BATCH,
                        )
                    )

                    if course is None:
                        db.add(
                            Course(
                                college_id=college.id,
                                name=course_name,
                                batch=BATCH,
                            )
                        )
                        print(f"  Added course: {course_name}")
                    else:
                        print(f"  Course already exists: {course_name}")

            db.commit()
            print("\nTenant registration completed.")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    register_tenants()
