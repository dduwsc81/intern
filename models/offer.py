from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class Offer(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='オファーID')
    car_id = Column(BigInteger, nullable=False, comment='車両ID')
    # company_code = Column(String(13), comment='企業コード')

    register_sale_id = Column(BigInteger, comment='出品ID')
    # offer_out_user_id = Column(BigInteger , comment='オファー連絡者')
    offer_out_store_id = Column(String(13), comment='オファー連絡店舗')
    # offer_in_user_id = Column(BigInteger , comment='オファー受付者')
    offer_in_store_id = Column(String(13), comment='オファー受付店舗')

    offer_status = Column(Integer, comment='オファーステータス')
    hope_purchase_price = Column(Integer, comment='購入希望金額')
    # chat_channel_id = Column(String(50) , comment='チャットチャネルID')
    # chat_group_id = Column(String(50) , comment='チャットグループID')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')