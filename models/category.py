from sqlalchemy import Column, Integer, String, Date

from db.base_class import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    cat_name = Column(String(255), nullable=False)
