from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Date
from app.db.base_class import Base


class RegisterSale(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='出品ID')
    car_id = Column(BigInteger, nullable=False, comment='車両ID')
    company_code = Column(String(13), comment='企業コード')
    register_sale_type = Column(Integer, comment="出品種類")
    period_from = Column(DateTime, nullable=False, comment='出品期間FROM')
    period_to = Column(DateTime, nullable=False, comment='出品期間TO')

    # div = Column(Integer, comment="出品方式")
    hope_sale_base_price = Column(Integer, nullable=False, comment='出品希望価格(本体)')
    hope_sale_total_price = Column(Integer, comment='出品希望価格(総額)')
    buy_now_base_price = Column(Integer, comment='即決価格(本体)')
    buy_now_total_price = Column(Integer, comment='即決価格(総額)')

    hope_sale_base_price_tax = Column(Integer, nullable=False, comment='出品希望価格(本体)（税込）')
    hope_sale_total_price_tax = Column(Integer, nullable=False, comment='出品希望価格(総額)（税込）')
    buy_now_base_price_tax = Column(Integer, nullable=False, comment='即決価格(本体)（税込）')
    buy_now_total_price_tax = Column(Integer, nullable=False, comment='即決価格(総額)（税込）')

    price_type = Column(Integer, comment='価格タイプ')
    cust_agree_flg = Column(Integer, comment='顧客同意フラグ')
    register_sale_status = Column(Integer, comment='出品ステータス')
    assess_request_flg = Column(Integer, comment='査定希望フラグ')
    assess_id = Column(Integer, comment="査定ID")
    estimate_id = Column(Integer, comment="見積ID")

    platform_fee = Column(Integer, comment="プラットフォーム料金")
    brokerage_fee = Column(Integer, comment="仲介手数料")
    transfer_total_amount = Column(Integer, comment="振込総額")
    tax_rate = Column(Integer, comment="税率")
    platform_fee_tax = Column(Integer, comment="プラットフォーム料金（税込）")
    brokerage_fee_tax = Column(Integer, comment="仲介手数料（税込）")
    transfer_total_amount_tax = Column(Integer, comment="振込総額（税込）")

    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
    update_id = Column(BigInteger, nullable=False, comment='登録者')
    update_at = Column(DateTime, nullable=False, comment='更新日時')
    delete_id = Column(BigInteger, comment='削除日時')
    delete_at = Column(DateTime, default=None, comment='削除者')
    delete_flag = Column(Integer, index=True, default=0, nullable=False, comment='削除フラグ')