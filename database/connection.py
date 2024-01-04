# connection.py
from multiprocessing import process
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


load_dotenv()

DATABASE_URL = os.getenv('DB_URL')

if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL set for the connection.")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

