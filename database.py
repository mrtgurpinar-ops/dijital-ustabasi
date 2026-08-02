import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.getenv("STORAGE_DIR") or os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

raw_db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")

if raw_db_url:
    # Railway postgres URL fix (postgres:// -> postgresql://)
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = raw_db_url
    try:
        engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)
    except Exception as e:
        print("[Database Engine Warning] Failed with default driver, attempting pg8000 fallback:", e)
        pg8000_url = raw_db_url.replace("postgresql://", "postgresql+pg8000://", 1)
        engine = create_engine(pg8000_url, pool_size=10, max_overflow=20, pool_pre_ping=True)
else:
    db_path = os.path.join(STORAGE_DIR, "database.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
