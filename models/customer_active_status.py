from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, Numeric, String

from app.db.base_class import Base


class CustomerActiveStatus(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="ID"
    )
    company_code = Column(String(13), comment="企業コード")
    customer_code = Column(String(13), comment="顧客コード")
    active_status = Column(
        String(13), comment="アクティブステータス：最終取引日 24ヶ月以上: 0, 最終取引日 6~24ヶ月未満: 1, 6ヶ月未満: 2"
    )
    maintenance_sales_recording_date = Column(Date, comment="整備最終取引日")
    car_sales_recording_date = Column(Date, comment="車販最終取引日")
    recency_score = Column(Integer, comment="最終取引日スコア")
    maintenance_frequency = Column(Integer, comment="整備利用回数")
    car_sales_frequency = Column(Integer, comment="車販利用回数")
    frequency_score = Column(Integer, comment="利用回数スコア")
    maintenance_monetary = Column(Numeric(15, 0), comment="整備利用金額")
    car_sales_monetary = Column(Numeric(15, 0), comment="車販利用金額")
    monetary_score = Column(Integer, comment="利用金額スコア")
    total_score = Column(Integer, comment="全体スコア")
    rank = Column(Integer, comment="ランク")
    insert_at = Column(DateTime, default=None, comment="登録日時")
    update_at = Column(DateTime, default=None, comment="更新日時")
