from sqlalchemy import Column, String, DateTime, BigInteger

from app.db.base_class import Base


class SurveyUrlSetting(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_code = Column(String(13), nullable=False)
    store_code = Column(String(13), nullable=False)
    service_code = Column(String(13))
    menu_id = Column(String(13))
    survey_url_full = Column(String(1000), nullable=False)
    survey_url_short = Column(String(255), nullable=False)
    insert_id = Column(BigInteger, nullable=False, comment='登録者')
    insert_at = Column(DateTime, nullable=False, comment='登録日時')
