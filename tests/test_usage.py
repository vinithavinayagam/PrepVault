from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.usage as usage
from app.database import Base


def test_usage_tracking(monkeypatch, tmp_path):
    test_db = tmp_path / "test_usage.db"

    test_engine = create_engine(
        f"sqlite:///{test_db.as_posix()}",
        connect_args={"check_same_thread": False},
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    monkeypatch.setattr(usage, "SessionLocal", TestSessionLocal)

    usage.record_usage("success")
    usage.record_usage("success")
    usage.record_usage("failed")

    result = usage.get_usage()

    assert result["total_requests"] == 3
    assert result["successful_requests"] == 2
    assert result["failed_requests"] == 1

    test_engine.dispose()
