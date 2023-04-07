from sqlalchemy import BigInteger, Column, Integer, String

from app.db.base_class import Base


class StandardIncentive(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    code_type_id = Column(BigInteger, nullable=False, comment="コードタイプID")
    send_incentive_standard_tax = Column(Integer, nullable=False, comment="送客元標準インセンティブ")
    fg_incentive_standard_tax = Column(Integer, nullable=False, comment="FG標準インセンティブ")