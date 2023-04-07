from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class MCompany(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='企業マスタID')
    company_code = Column(String(13), nullable=False, comment='企業コード')

    owner_staff_code = Column(String(13), comment='オーナーコード')
    company_name = Column(String(255), nullable=False, comment='cognitoID')
    company_representative = Column(String(255), nullable=False, comment='代表者名')
    zip_code = Column(String(255), comment='郵便番号')
    prefectures_code = Column(String(13), comment='住所（都道府県）')

    address1 = Column(String(255), comment='住所（市区町村）')
    address2 = Column(String(255), comment='住所（番地）')
    address3 = Column(String(255), comment='住所（建物名）')
    phone_number = Column(String(255), nullable=False, comment='電話番号')
    email = Column(String(255), nullable=False, comment='メールアドレス')
    employee_count = Column(Integer, nullable=False, comment='社員数')
    shop_count = Column(Integer, nullable=False, comment='店舗数')
    first_month_of_the_year = Column(Integer, nullable=False, comment='期初月')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')