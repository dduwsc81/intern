from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date, Numeric
from app.db.base_class import Base


class ActivityMemo(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='ID')
    car_id = Column(BigInteger, nullable=False, comment='車両ID')

    memo_editor = Column(String(255), nullable=False, comment='入力者')
    comment = Column(String, nullable=False, comment='コメント')

    memo_create_at = Column(DateTime, nullable=False, comment='活動メモの登録日')
    insert_id = Column(Integer, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(Integer, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(Integer, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')


