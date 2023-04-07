from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class ActivityLog(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='logID')
    send_customer_id = Column(BigInteger, nullable=False, comment='送客ID')

    status = Column(Integer, nullable=False, comment='ステータス')
    comment = Column(String(512), nullable=False, comment='コメント')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')