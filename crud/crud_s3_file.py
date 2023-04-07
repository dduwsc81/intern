from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.constants import Const
from app.crud.base import CRUDBase
from fastapi import HTTPException, status
from app.models.s3_file import S3File
from app.schemas.s3_file import S3FileCreate, S3FileUpdate


class CRUDS3File(CRUDBase[S3File, S3FileCreate, S3FileUpdate]):

    # Create a new s3 file
    def create_s3_file(self, db: Session, *, obj_in: S3FileCreate, user_id) -> Any:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            insert_id=user_id,
            insert_at=datetime.utcnow(),
            update_id=user_id,
            update_at=datetime.utcnow(),
            delete_flag=Const.DEL_FLG_NORMAL
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_s3_file(self, db:Session, id: int, key: str):
        db_obj = db.query(S3File).filter(S3File.id == id, S3File.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'S3File s3_file_id {id} not found')
        db_obj.key = key
        db_obj.update_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_old_key(self, db: Session, id: int):
        db_obj = db.query(S3File).filter(S3File.id == id, S3File.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'S3File s3_file_id {id} not found')
        return db_obj.key


s3file = CRUDS3File(S3File)
