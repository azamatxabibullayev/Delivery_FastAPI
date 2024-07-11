from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:2005@localhost/fastapi"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
SesionLocal = sessionmaker(autocommit=False, autoflush=False)
