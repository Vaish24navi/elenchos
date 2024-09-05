from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URI = getenv("DATABASE_URI")

if DATABASE_URI is None:
    raise ValueError("DATABASE_URI environment variable is not set")

engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()