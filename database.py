import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.getenv("STORAGE_DIR") or os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

raw_db_url = (
    os.getenv("DATABASE_URL")
    or os.getenv("POSTGRES_URL")
    or os.getenv("POSTGRESQL_URL")
    or os.getenv("DATABASE_PUBLIC_URL")
)

if not raw_db_url:
    pghost = os.getenv("PGHOST")
    pguser = os.getenv("PGUSER") or "postgres"
    pgpass = os.getenv("PGPASSWORD")
    pgdb = os.getenv("PGDATABASE") or "railway"
    pgport = os.getenv("PGPORT") or "5432"
    if pghost and pgpass:
        raw_db_url = f"postgresql://{pguser}:{pgpass}@{pghost}:{pgport}/{pgdb}"

if raw_db_url:
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = raw_db_url
    DB_ENGINE_TYPE = "PostgreSQL"
    IS_PERSISTENT = True
    try:
        engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)
    except Exception as e:
        print("[Database Engine Warning] Default driver failed, using pg8000 fallback:", e)
        pg8000_url = raw_db_url.replace("postgresql://", "postgresql+pg8000://", 1)
        engine = create_engine(pg8000_url, pool_size=10, max_overflow=20, pool_pre_ping=True)
else:
    db_path = os.path.join(STORAGE_DIR, "dijital_ustabasi.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    DB_ENGINE_TYPE = "SQLite"
    IS_PERSISTENT = True
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
