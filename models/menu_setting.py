from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date, Text
from app.db.base_class import Base


class MenuSetting(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='メニューId')
    code_type_id = Column(BigInteger, nullable=False, comment='コードタイプId')
    reservation_data_type = Column(Integer, default=None, nullable=False, comment='予約データタイプ')
    paid_type = Column(Integer, default=None, nullable=False, comment='取引方法')

    menu_name = Column(String(255), nullable=False, comment='メニュー名')
    menu_content = Column(String(255), nullable=False, comment='メニュー内訳')

    menu_user_price = Column(Integer, comment='メニュー顧客金額')
    customer_guide_flag = Column(Integer, comment='カスタマーガイドフラグ')
    menu_send_incentive = Column(Integer, comment='メニュー送客元インセンティブ')
    menu_fg_incentive = Column(Integer, comment='メニューFGインセンティブ')
    incentive_flag = Column(Integer, default=1, nullable=False, comment='インセンティブフラグ')
    menu_time_require = Column(Integer, comment='メニュー所要時間')
    specify_location = Column(Integer, comment='場所を指定')
    shortest_available_day = Column(Integer, comment='利用可能な最小日数')

    from_store_code = Column(String(13), comment='依頼店舗コード')
    from_company_code = Column(String(13), comment='依頼元企業コード')
    menu_candidate_time = Column(String(13), nullable=True)

    send_email_flag = Column(Integer, nullable=False)
    schedule_consult_flag = Column(Integer, nullable=False)

    policy_type = Column(String(1), nullable=True, comment='text:0 url:1 pdf:2')
    policy_content = Column(Text, nullable=True)
    terms_type = Column(String(1), nullable=True, comment='text:0 url:1 pdf:2')
    terms_content = Column(Text, nullable=True)
    policy_pdf_file_name = Column(String(255), nullable=True)
    term_pdf_file_name = Column(String(255), nullable=True)
    email_optional_flag = Column(Integer, nullable=True)
    hide_checkout_language = Column(Integer, nullable=True)
    hide_store_information = Column(Integer, nullable=True)
    calendar_selection_detail = Column(String(256), nullable=True)
    schedule_consultation_detail = Column(String(256), nullable=True)

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')
