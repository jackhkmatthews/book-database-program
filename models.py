import logging
import os

from dotenv import load_dotenv
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


engine = create_engine(os.getenv("DATABASE_URL"), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column("Title", String)
    author = Column("Author", String)
    published_date = Column("Published", Date)
    price = Column("Price", Integer)

    def __repr__(self):
        return f"Title: {self.title} Author: {self.author} Published: {self.published_date} Price: {self.price}"
