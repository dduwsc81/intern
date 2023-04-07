from sqlalchemy import BigInteger, Column, Integer, String, DateTime

from app.db.base_class import Base


class MMailFormat(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    div = Column(Integer, comment="区分")
    template_type = Column(Integer)
    title = Column(String(128))
    content = Column(String(10000))

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
