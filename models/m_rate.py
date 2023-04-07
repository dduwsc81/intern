from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from app.db.base_class import Base


class MRate(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='メニューId')
    div = Column(Integer, comment='タイプ')
    rate = Column(Integer, default=0, nullable=False, comment='率')
    from_apply_at = Column(DateTime, default=None, nullable=False, comment='適用開始日')
    to_apply_at = Column(DateTime, default=None, comment='適用終了日')
    apply_company_cd = Column(String(255), nullable=False, comment='運用企業コード')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')
