from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String

from app.db.base_class import Base


class CarMarket(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    car_id = Column(BigInteger, index=True, nullable=False, comment="車両ID")
    store_code = Column(String(13), index=True, nullable=False, comment="店舗コード")
    car_status = Column(Integer, comment="車両ステータス")
    car_active_status = Column(Integer, comment="アクティブステータス")

    offer_cnt = Column(Integer, comment="オファー数")
    like_cnt = Column(Integer, comment="いいね数")
    view_detail_cnt = Column(Integer, comment="詳細閲覧数")
    prefectures_cd = Column(String(20), comment="都道府県コード")

    hide_flag = Column(Integer, comment="非表示フラグ")
    repair_history_flag = Column(Integer, comment="修復歴フラグ")
    duplication_flg = Column(Integer, comment="重複フラグ")
    displacement_power = Column(String(254), comment="総排気量又は定格出力")
    car_shape = Column(String(254), comment="車体の形状")

    door_number = Column(Integer, comment="ドア数")
    has_sr = Column(Integer, comment="SR（有無")
    has_navi = Column(Integer, comment="ナビ（有無")
    maintenance = Column(String(254), comment="整備")
    rating_score = Column(String(13), comment="評価点")
    interior = Column(String(254), comment="内装")
    drive = Column(String(254), comment="駆動")
    shift = Column(String(254), comment="シフト")
    body_type = Column(String(254), comment="ボディタイプ")
    color_code = Column(String(10))
    color_name = Column(String(254), comment="カラー（名／コード")

    has_kawa = Column(Integer, comment="カワ")
    common_dh = Column(Integer, comment="D並")
    handle_type = Column(Integer, comment="ハンドル")
    change_mode = Column(String(254), comment="チェンジ")
    new_car_price = Column(Float, comment="新車価格")

    seats_cnt = Column(Integer, comment="乗車定員")
    fuel = Column(String(128), comment="使用燃料")
    fuel_economy = Column(String(128), comment="燃費（WLTC）")
    tire_type = Column(String(128), comment="タイヤの種類")
    cold_region_spec = Column(Integer, comment="寒冷地仕様")
    key_cnt = Column(Integer, comment="キーの本数")
    one_onwer_flg = Column(Integer, comment="ワンオーナー")
    no_smoking_car_flg = Column(Integer, comment="禁煙車")
    garage = Column(String(64), comment="車庫情報（屋内外）")
    periodic_inspection_record_book = Column(Integer, comment="定期点検記録簿")
    registered_car_flg = Column(Integer, comment="登録済未使用車")
    import_type = Column(Integer, comment="国産/輸入(正規・並行)")
    dealer_car_flg = Column(Integer, comment="ディーラー車")
    check_car = Column(String(64), comment="現車確認")
    overall_evaluation = Column(Integer, comment="総合評価")
    exterior_evaluation = Column(Integer, comment="外装評価")
    interior_evaluation = Column(Integer, comment="内装評価")

    insert_id = Column(BigInteger, nullable=False, comment="登録者")
    insert_at = Column(DateTime, nullable=False, comment="登録日時")
    update_id = Column(BigInteger, nullable=False, comment="登録者")
    update_at = Column(DateTime, nullable=False, comment="更新日時")
    delete_id = Column(BigInteger, comment="削除日時")
    delete_at = Column(DateTime, default=None, comment="削除者")
    delete_flag = Column(
        Integer, index=True, default=0, nullable=False, comment="削除フラグ"
    )

    common_name = Column(String(254), comment="通称型式")
