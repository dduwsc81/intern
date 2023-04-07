from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class MYear(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='ID')

    display_text = Column(String(20), nullable=False, comment='表示テキスト')
    value = Column(Integer, nullable=False, comment='価値')
    order_index = Column(Integer, nullable=False, comment='表示順')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')