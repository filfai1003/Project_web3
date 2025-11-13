from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Using a local SQLite DB for simplicity. Change URL for production (Postgres, etc.).
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend_db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30},
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
