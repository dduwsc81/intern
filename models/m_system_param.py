from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class MSystemParam(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="ロールID"
    )

    div = Column(Integer, nullable=False, index=True, comment="区分")
    div_name = Column(String(128), nullable=False, index=True, comment="区分名")

    param1 = Column(Integer, comment="値1")
    param2 = Column(Integer, comment="値2")
    param3 = Column(Integer, comment="値3")

    desc1 = Column(String(512), comment="記述1")
    desc2 = Column(String(512), comment="記述2")
    desc3 = Column(String(512), comment="記述3")

    comment = Column(String(512), comment="コメント")

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
