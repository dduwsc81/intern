from sqlalchemy import Column, BigInteger, Integer, DateTime, String, Text

from app.db.base_class import Base


class MenuStoreLink(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='送客メニューリンクID')
    menu_id = Column(BigInteger, nullable=False, comment='メニューID')
    to_company_code = Column(String, comment='企業コード（依頼先）')
    to_store_code = Column(String, comment='店舗コード（依頼先）')
    sort_number = Column(Integer, comment='ソート順')
    reservable_time = Column(Text, comment='reservable_time')
    transfer_flag = Column(Integer, comment='乗換')
    vehicle_inspection_flag = Column(Integer, comment='車検')
    legal_inspection_flag = Column(Integer, comment='法定点検')
    periodic_inspection_flag = Column(Integer, comment='定期点検')
    oil_flag = Column(Integer, comment='オイル')
    battery_flag = Column(Integer, comment='バッテリー')
    tire_flag = Column(Integer, comment='タイヤ')
    insurance_flag = Column(Integer, comment='保険')
    loan_lease_flag = Column(Integer, comment='ローン・リース')
    birthday_flag = Column(Integer, comment='誕生日')
    in_household_acquaintance_flag = Column(Integer, comment='世帯内・知人')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='更新者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, default=None, comment='削除者')
    delete_at = Column(DateTime, default=None, comment='削除日時')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')