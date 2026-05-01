"""Database schema bootstrap for warehouse app."""

from __future__ import annotations

SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS products (
        sku TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        unit TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        change INTEGER NOT NULL CHECK(change <> 0),
        type TEXT NOT NULL CHECK(type IN ('IMPORT', 'EXPORT')),
        ref_type TEXT NOT NULL,
        ref_id INTEGER,
        created_at TEXT NOT NULL,
        FOREIGN KEY(sku) REFERENCES products(sku)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS hold_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('OPEN', 'DONE')),
        created_at TEXT NOT NULL,
        note TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS hold_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        returned_quantity INTEGER NOT NULL DEFAULT 0 CHECK(returned_quantity >= 0),
        status TEXT NOT NULL CHECK(status IN ('HOLD', 'RETURNED')),
        FOREIGN KEY(session_id) REFERENCES hold_sessions(id) ON DELETE CASCADE,
        FOREIGN KEY(sku) REFERENCES products(sku)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        hold_session_id INTEGER,
        created_at TEXT NOT NULL,
        note TEXT,
        FOREIGN KEY(hold_session_id) REFERENCES hold_sessions(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
        FOREIGN KEY(sku) REFERENCES products(sku)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stock_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_code TEXT UNIQUE NOT NULL,
        employee_name TEXT,
        transaction_date TEXT NOT NULL,
        area TEXT,
        description TEXT,
        sku TEXT NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        direction TEXT NOT NULL CHECK(direction IN ('IMPORT', 'EXPORT')),
        note TEXT,
        bill_return TEXT,
        address TEXT,
        phone TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(sku) REFERENCES products(sku)
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_ledger_sku ON ledger(sku);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_ledger_date ON ledger(created_at);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_hold_session ON hold_items(session_id);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_sales_created_at ON sales(created_at);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_stock_txn_date ON stock_transactions(transaction_date);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_stock_txn_sku ON stock_transactions(sku);
    """,
]
