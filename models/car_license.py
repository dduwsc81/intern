from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class CarLicense(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="免許証ID"
    )

    company_code = Column(String(13), nullable=False, comment="企業コード")
    customer_code = Column(String(13), nullable=False, comment="顧客コード")
    license_color = Column(String(13), comment="免許証の色")
    license_number = Column(String(13), comment="免許証番号")
    license_image_front = Column(String(13), comment="顧客免許証画像(表)")
    license_image_back = Column(String(13), comment="顧客免許証画像(裏)")

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
