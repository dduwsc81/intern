from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base_class import Base


class MService(Base):
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, comment="ID")
    service_cd = Column(String(10), comment='サービスコード')
    service_name = Column(String(256), comment='サービス名')
    category = Column(String(256), comment='カテゴリー')
    price = Column(Integer, nullable=False, comment="価格")
    order_index = Column(Integer, nullable=False, comment="表示順")
    description = Column(String, comment='説明')

    insert_id = Column(Integer, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時", default=datetime.now(timezone.utc))
    update_id = Column(Integer, nullable=False, comment="更新者")
    update_at = Column(
        DateTime,
        nullable=False,
        comment="更新日時",
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    delete_id = Column(Integer, comment="削除者")
    delete_at = Column(DateTime, default=None, comment="削除日時")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
