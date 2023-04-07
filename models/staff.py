from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class Staff(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='スタッフID')
    company_code = Column(String(13), nullable=False, comment='企業コード')
    staff_code = Column(String(13), nullable=False, comment='スタッフコード')
    cognito_id = Column(String(13), nullable=False, comment='cognitoID')

    cars_manager_id = Column(String(13), comment='cars_Manager_ID')
    staff_photo = Column(String(13), comment='スタッフ写真')
    last_name = Column(String(255), comment='姓')
    first_name = Column(String(255), comment='名')
    last_name_kana = Column(String(255), comment='姓カナ')
    first_name_kana = Column(String(255), comment='名カナ')

    birthday = Column(Date, comment='生年月日')
    phone_number = Column(String(255), comment='電話番号')
    email = Column(String(255), nullable=False, comment='メールアドレス')

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')