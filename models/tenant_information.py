from app.db.base_class import Base
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import String


class TenantInformation(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="InfomationID")
    base_url = Column(String(255), nullable=False, comment="base url")
    company_code = Column(String(13), nullable=False, unique=True, comment="company code")
    user_email = Column(String(255), nullable=False, comment="email")
    user_password = Column(String(255), nullable=False, comment="password")
