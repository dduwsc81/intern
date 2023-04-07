from sqlalchemy import Column, String, BigInteger, Text
from app.db.base_class import Base


class CarsRole(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='ロールID')
    # company_code = Column(String(13), index=True, comment='企業コード')
    role = Column(String(255), index=True, comment='ロール名')
    userpool_id = Column(Text, comment='ユーザープールID')