from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  
DB_PATH = (BASE_DIR / ".." / ".." / "data" / "library.db").resolve()
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  
)

SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
