from sqlalchemy import Column, String, BigInteger, Text, DateTime, Integer
from app.db.base_class import Base


class ChatGroup(Base):
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True, comment='ロールID')
    # group_id = Column(String(23), nullable=False, comment='グループID')
    offer_id = Column(BigInteger, nullable=False, comment='オファーID')
    car_id = Column(BigInteger, comment="車両ID")

    chassis_number = Column(String(255), comment='車台番号')
    div = Column(Integer, comment='区分')
    store_id = Column(String(13), comment='店舗ID')
    firebase_chat_id = Column(String(128), comment='firebaseグループチャットID')

    message_total_cnt = Column(Integer, comment='メッセージ数')
    last_message_user_name = Column(String(45), comment='最終送信ユーザー名')
    last_message_datetime = Column(DateTime, nullable=False, comment='最終送信日時')
    message_unread_cnt = Column(Integer, comment='メッセージ未読数')
    last_message_user_id = Column(BigInteger, comment='最終送信ユーザーID')
    last_message = Column(String(255), comment="最後のメッセージ")
    last_message_store_id = Column(BigInteger, comment="最終チャットした店舗ID")

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')