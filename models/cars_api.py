from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class CarsApi(Base):
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, unique=True, comment='APIID')
    company_code = Column(String(13), index=True, comment='企業コード')
    api_type = Column(String(255), comment='APIタイプ')
    operationid = Column(String(255), index=True, comment='オペレーションID')
