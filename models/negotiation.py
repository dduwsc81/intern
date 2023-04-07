from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, Integer

from app.db.base_class import Base


class Negotiation(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="ID"
    )

    car_id = Column(BigInteger, index=True, nullable=False, comment="車両ID")
    register_sale_id = Column(BigInteger, comment="出品ID")
    contact_id = Column(BigInteger, comment="連絡ID")
    estimate_id = Column(BigInteger, comment="見積ID")
    negotiation_store_id = Column(BigInteger, comment="商談店舗ID")
    owner_store_id = Column(BigInteger, comment="オーナー店舗ID")
    negotiation_status = Column(Integer, nullable=False, comment="オファーステータス")
    period_from = Column(DateTime, comment="商談期間_FROM")
    period_to = Column(DateTime, comment="商談期間_TO")

    insert_id = Column(Integer, nullable=False, comment="登録者")
    insert_at = Column(
        DateTime, nullable=False, comment="登録日時", default=datetime.now(timezone.utc)
    )
    update_id = Column(Integer, nullable=False, comment="登録者")
    update_at = Column(
        DateTime,
        nullable=False,
        comment="更新日時",
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    delete_id = Column(Integer, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
