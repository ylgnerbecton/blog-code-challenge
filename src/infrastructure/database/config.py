from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
