from sqlalchemy import Column, String, BigInteger, Text, DateTime, Integer, Date
from app.db.base_class import Base


class LikeDetail(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')
    car_id = Column(BigInteger, nullable=False, comment='車両ID')
    store_id = Column(String(13), index=True, nullable=False, comment='登録店舗ID')
    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='更新者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, nullable=True, comment='削除者')
    delete_at = Column(DateTime, nullable=True, comment='削除日時')
    delete_flag = Column(Integer, nullable=False, comment='削除フラグ')
