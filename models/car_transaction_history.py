from datetime import datetime, timezone

from sqlalchemy import BigInteger, Integer, Column, DateTime, String, Date

from app.db.base_class import Base


class CarTransactionHistory(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment='車両ID'
    )

    car_id = Column(BigInteger, nullable=False, comment="車両ID")
    company_code = Column(String(13), comment='企業コード')
    car_code = Column(String(13), comment='車両ID')
    transaction_date = Column(Date, comment='計上日')
    transaction_type = Column(Integer, comment='取引種別')
    contents = Column(String(255), comment='内容')

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
