import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import area, product, stock, user  # noqa: F401
from app.models.base import Base


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

