from sqlalchemy import create_engine, inspect, text

from app.core.config import get_settings
from app.core.database import initialize_database


def test_initialize_database_runs_alembic_migrations(monkeypatch, tmp_path):
    database_path = tmp_path / "inventory.db"
    monkeypatch.setenv("DATABASE_PATH", str(database_path))
    get_settings.cache_clear()
    try:
        initialize_database()

        engine = create_engine(f"sqlite:///{database_path}", future=True)
        inspector = inspect(engine)
        table_names = set(inspector.get_table_names())
        with engine.connect() as connection:
            version = connection.execute(text("select version_num from alembic_version")).scalar_one()

        assert database_path.exists()
        assert {"alembic_version", "products", "areas", "stock_documents", "stock_document_lines", "users"} <= table_names
        assert version == "0001_initial_schema"
    finally:
        get_settings.cache_clear()
