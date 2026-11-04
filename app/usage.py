from sqlalchemy import Column, Integer, String, func

from app.database import Base, SessionLocal


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)


def initialize_usage_db():
    Base.metadata.create_all(bind=SessionLocal.kw["bind"], tables=[UsageLog.__table__])


def record_usage(status: str):
    with SessionLocal() as db:
        usage = UsageLog(status=status)
        db.add(usage)
        db.commit()


def get_usage():
    with SessionLocal() as db:
        total = db.query(func.count(UsageLog.id)).scalar() or 0

        successful = db.query(func.count(UsageLog.id)).filter(UsageLog.status == "success").scalar() or 0

        failed = db.query(func.count(UsageLog.id)).filter(UsageLog.status == "failed").scalar() or 0

    return {
        "total_requests": total,
        "successful_requests": successful,
        "failed_requests": failed,
    }
