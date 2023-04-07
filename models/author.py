from sqlalchemy import Column, Integer, String, Date

from db.base_class import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    author_name = Column(String(255), nullable=False)
    author_age = Column(Integer, nullable=True)

