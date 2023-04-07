from sqlalchemy import Column, Integer, String, Date

from db.base_class import Base



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    book_name = Column(String(255), nullable=False)
    book_description = Column(String(255), nullable=True)
    created_at = Column(Date)
    author_id = Column(Integer, nullable=False)
    cat_id = Column(Integer, nullable=False)