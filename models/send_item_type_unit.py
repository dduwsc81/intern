from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class SendItemTypeUnit(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='コードマスタID')
    company_code = Column(String(13), nullable=False, comment='企業コード')
    send_item_type_code = Column(String(13), nullable=False, comment='送客案件種別コード')
    unit = Column(Integer, nullable=False, comment='単価')
    from_apply_at = Column(Date, default=None, comment='適用開始日')
    to_apply_at = Column(Date, default=None, comment='適用終了日')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')