from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class SearchCondition(Base):
    search_condition_id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="検索条件ID"
    )
    search_name = Column(String(512), nullable=False, comment="検索名")

    order_index = Column(Integer, comment="順位")
    store_id = Column(String(13), comment="店舗ID")
    search_tab_id = Column(Integer, comment="検索タブID")

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
