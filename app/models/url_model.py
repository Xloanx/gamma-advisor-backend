from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class URL(Base):
    """Table for storing URLs to scrape."""
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    last_scraped = Column(DateTime, default=func.now(), onupdate=func.now())

class ScrapedData(Base):
    """Table for storing scraped web content."""
    __tablename__ = "scraped_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())

