from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class SendCustomerChatGroup(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="logID")
    send_customer_id = Column(BigInteger, nullable=False, comment="送客ID")

    div = Column(Integer, nullable=False, comment="区分")
    company_code = Column(String(13), comment="企業コード")
    store_code = Column(String(13), nullable=False, comment="店舗コード")
    firebase_chat_id = Column(String(128), nullable=False, comment="登録者")

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
