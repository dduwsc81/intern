from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date, TIMESTAMP, TEXT
from sqlalchemy.sql import func
from app.db.base_class import Base


class SendCustomer(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='送客ID')
    send_customer_code = Column(String(13), index=True, comment='送客コード')
    from_company_code = Column(String(13), index=True, comment='企業コード（依頼元）')
    from_store_code = Column(String(13), comment='店舗コード（依頼元）')
    from_staff_code = Column(String(13), index=True, comment='スタッフコード（依頼元）')
    to_company_code = Column(String(13), index=True, comment='企業コード（依頼先）')
    to_store_code = Column(String(13), comment='店舗コード（依頼先）')
    customer_code = Column(String(13), index=True, comment='顧客コード')
    face_photo = Column(String(13), index=True, comment='顔写真')
    send_item_type_code = Column(String(13), index=True, comment='送客案件種別コード')

    customer_last_name = Column(String(255), comment='姓')
    customer_first_name = Column(String(255), comment='名')
    customer_last_name_kana = Column(String(255), comment='姓カナ')
    customer_first_name_kana = Column(String(255), comment='名カナ')

    customer_phone_number = Column(String(255), comment='電話番号')
    customer_cellphone_number = Column(String(255), comment='携帯電話')
    customer_email = Column(String(255), comment='メールアドレス')
    customer_zip_code = Column(String(255), comment='郵便番号')

    customer_prefectures_code = Column(String(13), comment='住所（都道府県）')
    car_code = Column(String(13), comment='車両コード')
    car_mileage = Column(Integer, comment='走行距離')

    customer_address1 = Column(String(255), comment='住所（市区町村）')
    customer_address2 = Column(String(255), comment='住所（番地）')
    customer_address3 = Column(String(255), comment='住所（建物名）')

    car_maker = Column(String(255), comment='メーカー')
    car_type = Column(String(255), comment='車種')
    car_grade = Column(String(255), comment='グレード')
    car_land_transport_office = Column(String(255), comment="陸運事務局名称")
    car_registration_number_type = Column(String(255), comment='車両登録番号（種別）')
    car_registration_number_kana = Column(String(255), comment='車両登録番号（カナ）')
    car_registration_number = Column(String(255), comment='車両登録番号（プレート番号）')

    car_mileage_registration_date = Column(DateTime, default=None, comment="走行距離登録日時")
    car_registration_first_date = Column(DateTime, default=None, comment='初度登録年月')
    car_registration_end_date = Column(DateTime, default=None, comment='車検満了日')

    send_customer_at = Column(TIMESTAMP, nullable=False, default=func.now(), comment='送客日時')

    content = Column(TEXT, comment='ご依頼内容')
    send_incentive = Column(Integer, comment='送客元インセンティブ')
    fg_incentive = Column(Integer, comment='FGインセンティブ')
    send_incentive_tax = Column(Integer, comment='送客元インセンティブ TAX')
    fg_incentive_tax = Column(Integer, comment='FGインセンティブ TAX')
    menu_user_price = Column(Integer, comment="オプション受け入れ金額")
    menu_user_price_tax = Column(Integer, comment="オプション受け入れ金額_TAX")
    option_user_price = Column(Integer, comment="オプション顧客金額")
    option_user_price_tax = Column(Integer, comment="オプション顧客金額_TAX")
    tax_rate = Column(Integer, comment="TAX_率")
    status_flag = Column(Integer, comment='ステータス')

    contact_option = Column(String(255), comment='ご連絡が可能な時間帯')
    reservation_time = Column(String(255), comment='予約日時')
    reservation_id = Column(Integer, comment="予約ID")
    paid_type = Column(Integer, default=None, nullable=False, comment='取引方法')
    reservation_classification = Column(
        String(255), default=None, nullable=False, comment="区分"
    )

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')