from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.service_fee import ServiceFee
from app.schemas.service_fee import ServiceFeeCreate, ServiceFeeUpdate, ServiceFeeRequest

from app import crud
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from fastapi import HTTPException, status


class CRUDServiceFee(CRUDBase[ServiceFee, ServiceFeeCreate, ServiceFeeUpdate]):

    def get_service_fee(
            self,
            db: Session,
            obj_in: ServiceFeeRequest
    ):
        company_code = obj_in.company_code if obj_in.company_code else None
        store_code = obj_in.store_code if obj_in.store_code else None
        list_service = crud.code_master.get_list_service(db)
        list_service_with_type = db.query(self.model).filter(ServiceFee.company_code == company_code,
                                                             ServiceFee.store_code == store_code,
                                                             ServiceFee.delete_flag == 0).all()
        list_service_fee = {}
        for service in list_service:
            list_service_fee_by_type = []
            for item in list_service_with_type:
                if item.code_type_id == service.code_value:
                    list_service_fee_by_type.append(item)
            list_service_fee[service.code_name] = list_service_fee_by_type
        return list_service_fee

    def create_service_fee(
            self,
            db: Session,
            *,
            obj_in: ServiceFeeCreate
    ):
        obj_in_data = jsonable_encoder(obj_in)

        # hard code insert_id , update_id
        insert_id = 88888
        update_id = 1
        db_obj = self.model(**obj_in_data, insert_id=insert_id, insert_at=datetime.utcnow(), update_id=update_id,
                            update_at=datetime.utcnow(), delete_flag=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_service_fee(
            self,
            db: Session,
            *,
            id: int
    ):
        service_fee_by_id = db.query(self.model).filter(ServiceFee.id == id, ServiceFee.delete_flag == 0).first()
        if not service_fee_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Service Fee id {id} not found')

        # hard code delete_id
        service_fee_by_id.delete_id = 88888

        # update delete_flag, delete_at
        service_fee_by_id.delete_flag = 1
        service_fee_by_id.delete_at = datetime.utcnow()
        db.add(service_fee_by_id)
        db.commit()
        db.refresh(service_fee_by_id)
        return service_fee_by_id

    def update_service_fee(
            self,
            db: Session,
            *,
            id: int,
            obj_in: ServiceFeeUpdate
    ):
        obj_in_data = jsonable_encoder(obj_in)
        service_fee_data = db.query(self.model).filter(ServiceFee.id == id, ServiceFee.delete_flag == 0).first()
        if not service_fee_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Service Fee id {id} not found')

        # hard code update_id
        service_fee_data.update_id = 88888

        # update data
        if isinstance(obj_in_data, dict):
            update_data = obj_in_data
        else:
            update_data = obj_in_data.dict(exclude_unset=True)
        for field in update_data:
            if field in update_data:
                setattr(service_fee_data, field, update_data[field])

        service_fee_data.update_at = datetime.utcnow()

        db.add(service_fee_data)
        db.commit()
        db.refresh(service_fee_data)

        return service_fee_data


service_fee = CRUDServiceFee(ServiceFee)
