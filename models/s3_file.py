from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date, Text
from app.db.base_class import Base


class S3File(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='S3ファイル管理ID')
    bucket_name = Column(String(255), nullable=False ,comment='バケット名')
    key = Column(Text, nullable=False ,comment='S3パス')

    insert_id = Column(BigInteger, nullable=False ,comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False ,comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False,  comment='削除フラグ')