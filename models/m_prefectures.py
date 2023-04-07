from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from app.db.base_class import Base


class MPrefectures(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='都道府県マスタID')
    province_id = Column(BigInteger, nullable= False, comment='地方ID')
    prefectures_code = Column(String(45), nullable= False, comment='都道府県コード')
    name = Column(String(45), nullable= False, comment='都道府県名')
    name_kana = Column(String(45), nullable= False, comment='都道府県名')
    sort_number = Column(String(45), nullable= False, comment='ソート順')
