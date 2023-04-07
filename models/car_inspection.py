from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, String

from app.db.base_class import Base


class CarInspection(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="車両ID"
    )

    car_id = Column(BigInteger, nullable=False, index=True, comment="車両ID")
    company_code = Column(String(13), nullable=False, comment="企業コード")
    car_code = Column(String(13), nullable=False, comment="車両ID")
    car_category = Column(String(254), comment="自動車の種別")
    purpose = Column(String(254), comment="用途")
    private_business = Column(String(254), comment="自家用・事業用")
    car_shape = Column(String(254), comment="車体の形状")
    passenger_capacity = Column(String(254), comment="乗車定員")
    maximum_payload = Column(String(254), comment="最大積載量")
    car_weight = Column(String(254), comment="車両重量")
    car_total_weight = Column(String(254), comment="車両総重量")
    car_length = Column(String(254), comment="長さ")
    car_width = Column(String(254), comment="幅")
    car_height = Column(String(254), comment="高さ")
    front_front_axle_weight = Column(String(254), comment="前前軸重")
    front_rear_axle_weight = Column(String(254), comment="前後軸重")
    rear_front_axle_weight = Column(String(254), comment="後前軸重")
    rear_rear_axle_weight = Column(String(254), comment="後後軸重")
    car_inspection_type = Column(String(254), comment="型式")
    engine_type = Column(String(254), comment="原動機の型式")
    displacement_power = Column(String(254), comment="総排気量又は定格出力")
    fuel_type = Column(String(254), comment="燃料の種類")
    type_number = Column(String(254), comment="型式指定番号")
    category_number = Column(String(254), comment="類別区分番号")
    registration_end_date = Column(Date, comment="有効期限")

    insert_id = Column(Integer, nullable=False, comment="登録者")
    insert_at = Column(
        DateTime, nullable=False, comment="登録日時", default=datetime.now(timezone.utc)
    )
    update_id = Column(Integer, nullable=False, comment="登録者")
    update_at = Column(
        DateTime,
        nullable=False,
        comment="更新日時",
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    delete_id = Column(Integer, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )
