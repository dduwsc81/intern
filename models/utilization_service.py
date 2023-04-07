from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class UtilizationService(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="ID"
    )
    car_id = Column(BigInteger, comment="車両ID")
    register_sale_id = Column(BigInteger, comment="出品ID")
    contact_id = Column(BigInteger, comment="連絡ID")
    negotiation_id = Column(BigInteger, comment="商談ID")
    utilization_datetime = Column(DateTime, nullable=False, comment="登録日時")
    business_store_id = Column(BigInteger, comment="作業店舗ID")
    business_user_id = Column(BigInteger, comment="作業ユーザーID")
    service_cd = Column(String(10), nullable=False, comment='サービスコード')
    service_name = Column(String(256), comment='サービス名')
    receipt_amount = Column(Integer, comment="受取金額")
    payment_amount = Column(Integer, comment="支払金額")
    div = Column(Integer, comment="区分: 1: 購入、２：売却")

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
