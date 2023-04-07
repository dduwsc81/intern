from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class Assess(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="車両ID"
    )
    car_id = Column(BigInteger, nullable=False, index=True, comment="車両ID")

    company_code = Column(String(13), nullable=False, comment="企業コード")
    assess_status = Column(Integer, nullable=False, comment="査定ステータス")
    assess_store_id = Column(Integer, comment="査定店舗ID")
    assess_store_name = Column(String(128), comment="査定店舗名")
    assess_user_id = Column(Integer, comment="査定担当者")
    assess_user_name = Column(String(64), comment="査定担当者名")
    assess_price = Column(BigInteger, comment="査定価格")
    expiration_date = Column(DateTime, comment="有効期限")
    approve_user_id = Column(BigInteger, comment="承認担当者")
    assess_comment = Column(String(512), comment="査定コメント")
    assess_datetime = Column(DateTime, comment="査定日時")

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
