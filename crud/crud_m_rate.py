from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_rate import MRate
from datetime import date
from fastapi.encoders import jsonable_encoder


class CRUDMRate(CRUDBase[MRate, None, None]):
    M_RATE_TYPE = 1  # tax rate
    TAX_RATE_DEFAULT = 0

    def get_tax_rate(
            self, db: Session,
    ) -> Any:
        list_tax_rate = db.query(MRate).filter(MRate.delete_flag == 0, MRate.div == self.M_RATE_TYPE,
                                               MRate.from_apply_at <= date.today()).all()
        for tax_rate in list_tax_rate:
            if tax_rate.to_apply_at and tax_rate.to_apply_at < date.today():
                list_tax_rate.remove(tax_rate)
        tax_rate = list_tax_rate[len(list_tax_rate)-1] if list_tax_rate else None
        tax_rate = jsonable_encoder(tax_rate)
        return tax_rate


m_rate = CRUDMRate(MRate)
