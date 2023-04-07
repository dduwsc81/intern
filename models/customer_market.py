from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from app.db.base_class import Base
from datetime import datetime, timezone


class CustomerMarket(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='ID')
    company_code = Column(String(13), comment='企業コード')
    customer_code = Column(String(13), comment='顧客コード')
    insurance_class = Column(String(64), comment='保険等級')
    decade_age = Column(String(13), comment='年代')
    license_color = Column(String(13), comment='免許証の色')
    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(
        DateTime, nullable=False, comment="登録日時", default=datetime.now(timezone.utc)
    )

    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(
        DateTime,
        nullable=False,
        comment="更新日時",
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
