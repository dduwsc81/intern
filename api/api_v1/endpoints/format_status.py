from datetime import datetime, timezone, timedelta
from dateutil import parser
import json
from fastapi.responses import JSONResponse
import re

HALFWIDTH_TO_FULLWIDTH = str.maketrans(
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~',
    '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～')


# format response sales_period_start
def format_response_sales_period_start(date):
    date = date[0:4] + '-' + date[4:6] if date else ""
    return date


# format request sales_period_start
def format_request_sales_period_start(date):
    if date:
        date = date.replace("-", "")
    return date


# Convert ASCII chars to Unicode FULLWIDTH latin letters
def format_ascii_to_unicode(string):
    if string:
        string = string.translate(HALFWIDTH_TO_FULLWIDTH)
    return string


def jst_to_utc(local_time: str) -> str:
    dt = datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
    s = dt + timedelta(hours=-9)
    return str(s)


def utc_to_jst(strutc: str) -> str:
    str_utc = strutc.replace('T', ' ')
    dt = datetime.strptime(str_utc, '%Y-%m-%d %H:%M:%S')
    s = dt + timedelta(hours=+9)
    return str(s)


def format_gmt_to_utc_now(date):
    gmt_str = date.replace('+', '-')[:33] if '+' in date else date.replace('-', '+')[:33]
    date_parse = parser.parse(gmt_str)
    utc_time = date_parse.astimezone().strftime('%Y-%m-%d %H:%M:%S')
    return utc_time


# Return Response Header
def return_response_header(res):
    r = json.dumps(res)
    headers = {'Access-Control-Allow-Headers': 'Content-Type',
               'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': '*'}
    return JSONResponse(content=json.loads(r), headers=headers)


def convert_sort_key(origin_sortkey_list, key_dict, default_orderby_statement):
    """
    クエリパラメーターで渡ってきたCamel型のsortキーワードを
    SQLAlchemyまたは生SQLに合わせて変換。
    キーのすべてが無効なものだった場合はdefault_sortを返す
    注) リクエストは以下の形式を想定
    curl -X GET  "http://<URL>/v1/attractingCustomers/<storeCode>/<YYYYMM>?limit=1&sort=id&sort=outflow" -H 'Authorization: Bearer <トークン>’　# noqa: E501
    注)service側はsortキーを以下のtextに入れて使う
    from sqlalchemy.sql import text
    db.query(xx).order_by(text(sort))
    --------
    顧客一覧の場合)
    ■ origin_sortkey(パラメータのrequest.query.sort)
    ・"-customerCode" ⇒　"customer_code desc"
    ・"customerName"  ⇒　"last_name., first_name"
    ・"-customerName" ⇒ ""last_name desc, first_name desc
    ■key_dict ({クエリパラメーターのキー: [SQLのカラム]})
    key_dict = {"customerCode": ["customer_code"],
                "customerName": ["last_name", "first_name"],
                "registrationFirstDate": ["registration_first_date"],
                "registrationEndDate": ["registration_end_date"],
                "sellingDatetime": ["selling_datetime"]
                }
    ■ default_orderby_statement
    "customer_code"
    """

    orderby_statement = ""
    if not isinstance(origin_sortkey_list, list):
        tmp_origin_sortkey_list = []
        tmp_origin_sortkey_list.append(origin_sortkey_list)
        sort_key_list = tmp_origin_sortkey_list
    else:
        sort_key_list = origin_sortkey_list

    cnt = 1
    for k in sort_key_list:
        sort_direction = ""
        params_sort_key = k

        if k[:1] == "-":
            # キーの先頭が"-"の場合は、先頭のハイフン抜いて降順ソート
            sort_direction = "desc"
            params_sort_key = k[1:]

        if params_sort_key not in key_dict:
            # 指定外のソートキーを渡された場合は無視
            continue

        # クエリに適したソート用カラム名を取得(複数)
        converted_keys = key_dict[params_sort_key]

        for key in converted_keys:
            if cnt > 1:
                orderby_statement += ","

            orderby_statement += key + " " + sort_direction
            cnt += 1

    if len(orderby_statement) > 0:
        return orderby_statement
    else:
        return default_orderby_statement


def convert_camel_to_snake_case(name: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
