from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from app.db.base_class import Base


class Store(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='店舗ID')
    company_code = Column(String(13), nullable=False, comment='企業コード')

    area_code = Column(String(13), comment='地域ID')
    store_code = Column(String(13), nullable=False, comment='店舗コード')
    store_name = Column(String(255), nullable=False, comment='店舗名')

    external_system_store_name = Column(String(255), nullable=False, comment='外部システム 店舗名')
    zip_code = Column(String(255), comment='郵便番号')
    prefectures_code = Column(String(13), comment='住所（都道府県）')
    address1 = Column(String(255), comment='住所（市区町村）')
    address2 = Column(String(255), comment='住所（番地）')
    address3 = Column(String(255), comment='住所（建物名）')
    phone_number = Column(String(255), comment='電話番号')
    email = Column(String(255), comment='メールアドレス')
    reservation_available_lane = Column(Integer, comment='予約可能枠')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')