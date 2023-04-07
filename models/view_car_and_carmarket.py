from sqlalchemy import BigInteger, Column, Integer, String

from app.db.base_class import Base


class ViewCarAndCarmarket(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="車両ID"
    )
    store_code = Column(String(13), index=True, nullable=False, comment="店舗コード")
    result = Column(Integer, comment="車両ステータス / 乗換希望 / 乗換アラート / 未区分")
