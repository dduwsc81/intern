from sqlalchemy import Column, String, BigInteger, Text, DateTime, Integer
from app.db.base_class import Base


class ChatGroupMember(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='ID')
    group_id = Column(BigInteger, nullable=False, comment='グループID')
    store_id = Column(String(13), comment='店舗ID')
    user_id = Column(BigInteger, comment='ユーザーID')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')
