from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class Purchase(Base):
    purchase_id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="購入ID"
    )

    car_id = Column(BigInteger, index=True, nullable=False, comment="車両ID")
    negotiation_id = Column(BigInteger, comment="商談ID")
    status = Column(Integer, comment="ステータス")
    purchase_user_id = Column(BigInteger, comment="購入者ID")
    purchase_store_id = Column(BigInteger, comment="購入店舗ID")
    sale_approve_user_id = Column(BigInteger, comment="購入承諾者ID")
    sale_approve_store_id = Column(BigInteger, comment="購入承諾店舗ID")
    contract_datetime = Column(DateTime, comment="契約日時")
    close_datetime = Column(Integer, comment="クローズ日時")
    comment = Column(String(512), comment="コメント")

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True,  default=0, nullable=False, comment="削除フラグ"
    )
