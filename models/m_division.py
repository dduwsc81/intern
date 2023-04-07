from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class MDivision(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    div = Column(Integer, nullable=False, comment='区分')
    div_name = Column(String(128), comment='区分名')
    param = Column(Integer, comment='値')
    desc = Column(String(512), comment='記述')
    order_index = Column(Integer, comment='表示順')
    comment = Column(String(512), comment='コメント')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')
