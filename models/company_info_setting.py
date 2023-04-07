from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class CompanyInfoSetting(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    company_code = Column(String(13), index=True, nullable=False, comment="企業コード")
    s3_file_id = Column(BigInteger, comment="車両画像ファイルコード")
    company_name = Column(String(255), nullable=False, comment="会社名")
    company_name_display = Column(String(255), nullable=False, comment="会社名")
    sender_name = Column(String(255), nullable=False, comment="メール宛先")
    sender_mail = Column(String(255), nullable=False, comment="送信メールアドレス")
    hidden_company_name = Column(Integer, nullable=False)
    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
