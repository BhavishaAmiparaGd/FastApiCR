from sqlalchemy import Column, Integer, String
from database.connection import Base

class User(Base):
    __tablename__ = "item5"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))

