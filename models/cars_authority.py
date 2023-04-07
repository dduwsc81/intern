from sqlalchemy import Column, BigInteger
from app.db.base_class import Base


class CarsAuthority(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='権限ID')
    role_id = Column(BigInteger, index=True, comment='ロールID')
    api_id = Column(BigInteger, comment='APIID')
