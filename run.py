# run.py (for initial testing/migration)
from app.models.todo import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)
