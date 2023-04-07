from sqlalchemy import Column, BigInteger, Integer, DateTime, Date, String

from app.db.base_class import Base


class ServiceFee(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='サービスフィーID')
    code_type_id = Column(BigInteger, nullable=False, comment='コードタイプID')
    store_code = Column(String(13), comment='店舗コード')
    company_code = Column(String(13), comment='企業コード')
    send_incentive = Column(Integer, nullable=False, comment='送客元インセンティブ')
    fg_incentive = Column(Integer, nullable=False, comment='FGインセンティブ')
    from_apply_at = Column(Date, default=None, comment='適用開始日')
    to_apply_at = Column(Date, default=None, comment='適用終了日')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='更新者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, default=None, comment='削除者')
    delete_at = Column(DateTime, default=None, comment='削除日時')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')