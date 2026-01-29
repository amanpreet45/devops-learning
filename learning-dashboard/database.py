import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/dashboard")

engine = create_engine(DB_URL, pool_size=20, max_overflow=50, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()

def init_db():
    Path("uploads").mkdir(exist_ok=True)
    db = get_db()
    db.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TEXT DEFAULT ''
    );
    """))

    db.execute(text("""
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        status TEXT DEFAULT 'pending',
        txn_id TEXT DEFAULT '',
        screenshot_path TEXT DEFAULT '',
        created_at TEXT DEFAULT '',
        updated_at TEXT DEFAULT ''
    );
    """))

    # add indexes
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);"))

    db.commit()
    db.close()
