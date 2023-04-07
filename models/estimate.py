from datetime import datetime, timezone

from sqlalchemy import BigInteger, Integer, Column, DateTime

from app.db.base_class import Base


class Estimate(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment='車両ID'
    )
    car_id = Column(BigInteger, nullable=False, comment="車両ID")
    estimate_type = Column(Integer, comment='見積タイプ: 1:出品、2:購入')
    purchase_type = Column(Integer, comment='取引種別: 1:直接取引　2:仲介取引')
    purchase_store_id = Column(BigInteger, comment='取引店舗ID')
    hope_sale_base_price = Column(Integer, comment='出品希望価格(本体)')
    market_fee = Column(Integer, comment='マーケット手数料')
    brokerage_rate = Column(Integer, comment='仲介手数料割合')
    brokerage_fee = Column(Integer, comment='仲介手数料')
    margin_rate = Column(Integer, comment='マージン割合')
    margin_fee = Column(Integer, comment='マージン手数料')
    land_transportation_fee = Column(Integer, comment='陸送金額')
    name_change_fee = Column(Integer, comment='名義変更手数料')
    options_fee = Column(Integer, comment='オプション代')
    business_amount_type = Column(Integer, comment='事業金額種別')
    business_amount = Column(Integer, comment='事業金額')
    customer_amount_type = Column(Integer, comment='顧客金額種別')
    customer_amount = Column(Integer, comment='顧客金額')
    tax_rate = Column(Integer, default=10, comment='税率')
    hope_sale_base_price_tax = Column(Integer, comment='出品希望価格(本体)（税込）')
    market_fee_tax = Column(Integer, comment='マーケット手数料（税込）')
    land_transportation_fee_tax = Column(Integer, comment='陸送金額（税込）')
    name_change_fee_tax = Column(Integer, comment='名義変更手数料（税込）')
    option_fee_tax = Column(Integer, comment='オプション代（税込）')
    business_amount_tax = Column(Integer, comment='事業金額（税込）')
    customer_amount_tax = Column(Integer, comment='顧客金額（税込）')
    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(
        DateTime, nullable=False, comment="登録日時", default=datetime.now(timezone.utc)
    )
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(
        DateTime,
        nullable=False,
        comment="更新日時",
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
