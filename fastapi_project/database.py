from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase):
    pass

class Game(Base):
    __tablename__ = "Game"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), unique=True, nullable=False)
    cost = Column(Integer, unique=True, nullable=False)
    description = Column(Text(), unique=True, nullable=False)
    size = Column(Integer, default=datetime.utcnow)
    age_limited = Column(Integer, unique=True, nullable=False)

class Buyer(Base):
    __tablename__ = "Buyer"

    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    age = Column(Integer, default=True, nullable=False)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
