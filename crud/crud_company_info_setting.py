from typing import Any
from sqlalchemy.orm import Session

from app.constants import Const
from app.crud.base import CRUDBase
from app.models.company_info_setting import CompanyInfoSetting
from app.models.m_company import MCompany
from app.models.s3_file import S3File
from app.schemas.company_info_setting import CompanyInfoSettingCreate, CompanyInfoSettingUpdate, CompanyInfoSettingBase
from sqlalchemy import and_
from fastapi import HTTPException, status
from datetime import datetime
import boto3
import os


class CRUDCompanyInfoSetting(CRUDBase[CompanyInfoSetting, CompanyInfoSettingCreate, CompanyInfoSettingUpdate]):
    bucket_name = os.environ["BUCKET_NAME"]

    def get_company_information(self, db: Session, *, company_code: str) -> Any:
        domain_image = os.environ["DOMAIN_IMAGE"]
        company = db.query(MCompany).filter(MCompany.company_code == company_code,
                                            MCompany.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Company company code {company_code} not found")
        company_name = company.company_name
        company_information = (
            db.query(
                self.model.company_code,
                self.model.s3_file_id,
                self.model.company_name_display,
                self.model.company_name,
                self.model.sender_name,
                self.model.sender_mail,
                self.model.hidden_company_name
            ).filter(
                CompanyInfoSetting.company_code == company_code,
                CompanyInfoSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        )
        company_logo = ''
        company_name_display = ''
        sender_name = ''
        sender_mail = ''
        hidden_company_name = 0
        if company_information:
            if company_information.s3_file_id:
                s3_file = db.query(S3File).filter(S3File.id == company_information.s3_file_id,
                                                  S3File.delete_flag == Const.DEL_FLG_NORMAL).first()
                company_logo = str(domain_image) + str(s3_file.key)
            if company_information.company_name_display:
                company_name_display = company_information.company_name_display
            if company_information.company_name:
                company_name = company_information.company_name
            if company_information.sender_name:
                sender_name = company_information.sender_name
            if company_information.sender_mail:
                sender_mail = company_information.sender_mail
            if company_information.hidden_company_name:
                hidden_company_name = company_information.hidden_company_name
        company = {
            "company_name_display": company_name_display,
            "company_code": company_code,
            "company_name": company_name,
            "company_logo": company_logo,
            "sender_name": sender_name,
            "sender_mail": sender_mail,
            "hidden_company_name": hidden_company_name
        }
        return company

    def get_list_company_information(self, db: Session):
        list_company_info = db.query(
            CompanyInfoSetting,
            S3File.bucket_name,
            S3File.key
        ). \
            outerjoin(S3File, and_(CompanyInfoSetting.s3_file_id == S3File.id,
                                   S3File.delete_flag == Const.DEL_FLG_NORMAL)). \
            filter(CompanyInfoSetting.delete_flag == Const.DEL_FLG_NORMAL).all()
        return list_company_info

    def update_company_name_display(
            self, db: Session, *, company_code: str, company_name_display: str, is_delete_logo: int, sender_name: str,
            sender_mail: str, hidden_company_name: int
    ) -> Any:
        db_obj = db.query(self.model).filter(CompanyInfoSetting.company_code == company_code,
                                             CompanyInfoSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            db_obj = self.model(
                **{"company_code": company_code},
                insert_id=1,
                insert_at=datetime.utcnow(),
                update_id=1,
                update_at=datetime.utcnow(),
                delete_flag=Const.DEL_FLG_NORMAL)
        if company_name_display:
            db_obj.company_name_display = company_name_display
        else:
            db_obj.company_name_display = None
        if sender_name:
            db_obj.sender_name = sender_name
        else:
            db_obj.sender_name = None
        if sender_mail:
            db_obj.sender_mail = sender_mail
        else:
            db_obj.sender_mail = None
        db_obj.hidden_company_name = hidden_company_name
        db_obj.company_name = self.get_company_name(db=db, company_code=company_code)
        if is_delete_logo:
            db_obj.s3_file_id = None
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_company_name(
            self, db: Session, *, company_code: str
    ) -> Any:
        db_obj = db.query(MCompany).filter(MCompany.company_code == company_code,
                                           MCompany.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Company company code {company_code} not found")
        company_name = db_obj.company_name
        return company_name

    def update_company_logo(
        self, db: Session, *, company_code: str, s3_file_id: int
    ) -> Any:
        db_obj = db.query(CompanyInfoSetting).filter(CompanyInfoSetting.company_code == company_code,
                                           CompanyInfoSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            db_obj = self.model(
                **{"company_code": company_code},
                insert_id=1,
                insert_at=datetime.utcnow(),
                update_id=1,
                update_at=datetime.utcnow(),
                delete_flag=Const.DEL_FLG_NORMAL, )
        db_obj.s3_file_id = s3_file_id
        db_obj.company_name = self.get_company_name(db=db, company_code=company_code)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_company_information(
            self, db: Session, company_code: str
    ):
        db_obj = db.query(CompanyInfoSetting).filter(CompanyInfoSetting.company_code == company_code,
                                                     CompanyInfoSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Request is invalid or parameters are incorrect")
        db_obj.delete_flag = Const.DEL_FLG_DELETE
        db_obj.delete_at = datetime.utcnow()
        db.add(db_obj)

        # Delete record s3_file
        if db_obj.s3_file_id:
            s3_file = db.query(S3File).filter(S3File.id == db_obj.s3_file_id,
                                              S3File.delete_flag == Const.DEL_FLG_NORMAL).first()
            if not s3_file:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'S3 file s3_file_id {db_obj.s3_file_id} not found')
            s3_file.delete_flag = Const.DEL_FLG_DELETE
            s3_file.delete_at = datetime.utcnow()
            db.merge(s3_file)

            # Delete S3 File
            self.delete_file(self.bucket_name, s3_file.key)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_file(self, del_bucket, del_key):
        s3 = boto3.resource("s3")
        s3.Object(del_bucket, del_key).delete()

    def check_company_logo(self, db, company_code):
        company_logo = db.query(CompanyInfoSetting).filter(CompanyInfoSetting.company_code == company_code,
                                                           CompanyInfoSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if company_logo and company_logo.s3_file_id:
            return company_logo.s3_file_id
        else:
            return None


company_info_setting = CRUDCompanyInfoSetting(CompanyInfoSetting)
