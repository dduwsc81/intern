from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class CodeMaster(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='コードマスタID')
    code_type = Column(String(255), nullable=False, comment='種別')
    code_value = Column(Integer, nullable=False, comment='コード値')
    code_name = Column(String(255), nullable=False, comment='表示名')
    sort_number = Column(Integer, comment='ソート順')