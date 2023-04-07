import json
import requests
import base64
from fastapi import HTTPException
from app.constants import Const

session = requests.Session()
REQUEST_TIMEOUT = 30
HttpMethod = Const.HttpMethod


def session_option(http_type, url, data=None, list_data=None, params=None,
                   authorization=None):
    status_code = 200
    if http_type == HttpMethod.GET:
        res = session.get(
            url=url,
            headers={"authorization": authorization},
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    elif http_type == HttpMethod.POST:
        res = session.post(
            url=url,
            headers={"authorization": authorization},
            json=data,
            data=list_data,
            timeout=REQUEST_TIMEOUT,
        )
    elif http_type == HttpMethod.PUT:
        res = session.put(
            url=url,
            headers={"authorization": authorization},
            json=data,
            timeout=REQUEST_TIMEOUT,
        )
    elif http_type == HttpMethod.DELETE:
        res = session.delete(
            url=url,
            headers={"authorization": authorization},
            json=data,
            timeout=REQUEST_TIMEOUT,
        )
    if res.status_code < 200 or res.status_code >= 300:
        status_code = res.status_code
        if status_code == 401:
            raise HTTPException(
                status_code=status_code,
                detail="token unauthorized")
        raise HTTPException(
            status_code=status_code,
            detail="Request is invalid or parameters are incorrect",
        )
    return res


def call_api(http_type, url, token, data=None, list_data=None, params=None):
    res = session_option(
        http_type=http_type,
        url=url,
        params=params,
        data=data,
        list_data=list_data,
        authorization=token
    )
    return json.loads(res.text)


def encode_btoa(raw_string):
    dataBytes = raw_string.encode("utf-8")
    encoded = base64.b64encode(dataBytes)
    return encoded.decode('ascii')
