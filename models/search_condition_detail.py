from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .search_condition import SearchCondition  # noqa: F401


class SearchConditionDetail(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    search_condition_id = Column(BigInteger, nullable=False, comment="検索条件ID")

    condition_name = Column(String(50), comment="条件項目名")
    condition_type = Column(String(10), comment="条件区分")
    values = Column(String(10000), comment="検索値")

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
