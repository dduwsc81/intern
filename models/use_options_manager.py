from datetime import datetime, timezone

from sqlalchemy import BigInteger, Integer, Column, DateTime, String

from app.db.base_class import Base


class UseOptionsManager(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment='車両ID'
    )
    car_id = Column(BigInteger, nullable=False, comment="車両ID")
    estimate_id = Column(BigInteger, comment='見積ID')
    option_id = Column(BigInteger, comment='オプションID')
    option_name = Column(String(256), comment='オプション名')
    option_packet_id = Column(BigInteger, comment='オプションパケットID')
    option_packet_name = Column(String(256), comment='オプションパケット名')
    option_fee = Column(Integer, comment='オプション代')
    option_fee_tax = Column(Integer, comment='オプション代（税込）')
    option_content = Column(String(512), comment='オプション内容')
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
