from datetime import datetime, timezone

from sqlalchemy import BigInteger, Column, DateTime, Integer, String

from app.db.base_class import Base


class CarEquipmentDetails(Base):
    id = Column(
        BigInteger, primary_key=True, unique=True, autoincrement=True, comment="車両ID"
    )
    car_id = Column(BigInteger, nullable=False, index=True, comment="車両ID")

    etc = Column(Integer, comment="ETC")
    navi = Column(Integer, comment="カーナビ")
    apple_carplay = Column(Integer, comment="Apple CarPlay")
    audroid_auto = Column(Integer, comment="Android Auto")
    bluetooth_connect = Column(Integer, comment="Bluetooth接続")
    usb_input_device = Column(Integer, comment="USB入力端子")
    v_power_100 = Column('100V_power', Integer, comment="100V電源")
    drive_recorder = Column(Integer, comment="ドライブレコーダー")
    rear_seat_monitor = Column(Integer, comment="後席モニター")
    back_camera = Column(Integer, comment="バックカメラ")
    camera_360 = Column('360_camera', Integer, comment="360度カメラ")
    slide_door_left = Column(Integer, comment="スライドドア（L）")
    slide_door_right = Column(Integer, comment="スライドドア（R）")
    electric_rear_gate = Column(Integer, comment="電動リアゲート")
    airbag = Column(Integer, comment="エアバッグ")
    idling_stop = Column(Integer, comment="アイドリングストップ")
    anti_theft_device = Column(Integer, comment="盗難防止装置")
    sunroof = Column(Integer, comment="サンルーフ")
    roof_carrier = Column(Integer, comment="ルーフキャリア")
    roof_box = Column(Integer, comment="ルーフボックス")
    leather_seat = Column(Integer, comment="レザーシート")
    row_seat_3 = Column('3row_seat', Integer, comment="3列シート")
    seat_heater = Column(Integer, comment="シートヒーター")
    seat_cooler = Column(Integer, comment="シートクーラー")
    full_flat_sheet = Column(Integer, comment="フルフラットシート")
    cruise_control = Column(Integer, comment="クルーズコントロール")
    cruise_control_following = Column(Integer, comment="クルーズコントロール（追従型）")
    autopilot = Column(Integer, comment="オートパイロット")
    lane_keep_assist = Column(Integer, comment="レーンキープアシスト")
    parking_assist = Column(Integer, comment="パーキングアシスト")
    obstacle_sensor = Column(Integer, comment="障害物センサー")
    lane_departure_warning = Column(Integer, comment="車線逸脱警報")
    electronic_stability_control = Column(Integer, comment="横滑り防止装置")
    collision_damage_mitigation_brake = Column(Integer, comment="衝突被害軽減ブレーキ")
    prevention_false_start = Column(Integer, comment="誤発進防止")
    auto_light = Column(Integer, comment="オートライト")
    car_rental = Column(Integer, comment="レンタカー")
    test_drive = Column(Integer, comment="展示・試乗車")

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
