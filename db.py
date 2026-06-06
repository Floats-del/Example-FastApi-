from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import settings

# Construct PostgreSQL connection URL using production settings
DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
) 

# Configure engine with robust connection pooling policies
engine = create_engine(
    DATABASE_URL, #for postgres, but if u put, 'sqlite:///mydb.db' here then in same dir ull have db ;)
    pool_size=20, 
    max_overflow=10, 
    pool_timeout=30, 
    pool_recycle=3600
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine) 
Base = declarative_base()

def get_db():
    """Context manager dependency providing a clean transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()