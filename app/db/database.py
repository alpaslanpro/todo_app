from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.todo import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/todos_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)