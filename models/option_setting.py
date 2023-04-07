from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class OptionSetting(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='オプションID')
    group_id = Column(BigInteger, nullable=False, comment='グループID')
    option_name = Column(String(255), nullable=False, comment='オプション名')

    option_user_price = Column(Integer, comment='オプション顧客金額')
    option_content = Column(Integer, comment='オプション内訳')
    option_time_require = Column(Integer, comment='オプション所要時間')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')
