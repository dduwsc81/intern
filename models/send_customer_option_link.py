from sqlalchemy import Column, BigInteger, Integer, DateTime, Date

from app.db.base_class import Base


class SendCustomerOptionLink(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='送客メニューリンクID')
    option_id = Column(BigInteger, nullable=False, comment='オプションID')
    send_customer_id = Column(BigInteger, comment='送客ID')
    send_customer_option_price = Column(Integer, nullable=False, comment='送客オプション価格')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='更新者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, default=None, comment='削除者')
    delete_at = Column(DateTime, default=None, comment='削除日時')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')