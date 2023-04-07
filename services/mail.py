import re
import time
import uuid
import os
import tarfile
import shutil
import requests

from datetime import datetime
from dateutil import tz
from fastapi import HTTPException, status
from typing import Any, List, Optional

REG_EXP_PARAM_MESSAGE = r'{{+[a-z0-9_-]+}}'
REG_EXP_PARAM_URL = r'((?:\[\[??[^\[]*?\]\]))'
REGEX_MAIL = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(" \
             r"?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0" \
             r"b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-" \
             r"9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9" \
             r"]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-" \
             r"9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0" \
             r"b\x0c\x0e-\x7f])+)\])"  # noqa E501

CONTENT_MAIL = 'FromName=%(senders)s\r\n' \
               'From=%(sendersMail)s\r\n' \
               'Return=\nSubject=%(name)s\r\n' \
               '\r\n\r\n' \
               'MIME-Version: 1.0\r\n' \
               'Content-Type: text/html; charset="utf-8"\r\n' \
               'Content-Transfer-Encoding: 8bit \r\n' \
               '\r\n' \
               '<html>' \
               '<body>' \
               '%(body)s' \
               '{open_rate}' \
               '</body>' \
               '</html>'
TYPE_MAIL = 'PC-UTF8'
INTERVAL_MAIL = '100'
MAIL_CLIENT_ID = os.environ['API_MAIL_CLIENT_ID']
URL_MAIL = os.environ['API_MAIL_URL']
LIST_FILE = '%(taskId)s.list'
CONTENT_FILE = '%(taskId)s.conts'

SUCCESS = "Success"
FAIL = "Fail"

"""
Format of request:
{
    channels: string
    senders: string
    senders_mail: string
    template_subject:string
    body: string - template of body mail
    data: [
        {
            email: string,
            params: object
        }
    ]
}
"""

# Init session
session = requests.Session()


def send_mail(request) -> Any:
    # Convert template and send mail
    results = create_template_mail(request)

    return results


def create_template_mail(request):
    """ Apimailへの要求するテンプレートの準備　"""
    # Initialize data
    header: List = []
    contents = []
    dataSendMessages = request['data']
    channel = request['channels'].upper()
    body, bodyParams = replace_body_message(request['body'], channel)
    body = body.replace('\n', '<br>')
    body = replace_url(body)

    # Create task id with uuid
    taskId = uuid.uuid4().hex[:11]
    path = f'/tmp/{taskId}'
    listFile = LIST_FILE % {'taskId': taskId}
    contentFile = CONTENT_FILE % {'taskId': taskId}
    tarGzFile = f'{taskId}.tar.gz'
    tarGzDir = f'/tmp/{tarGzFile}'

    for element in dataSendMessages:
        # Check valid email
        if not check_valid_email(element["email"]):
            return f"{FAIL} - {element['email']}が不正です。"
        line = [element['email']]

        for param in bodyParams:
            # Get header contents of send mail
            if len(header) < len(bodyParams):
                header.append(param)
            # Get prams body for contents send mail
            line.append(replace_url(element['params'][param], isPersonalUrl=True))  # noqa E501
        contents.append(','.join(line))
    # Convert List to String
    header.insert(0, 'Email')
    header = [','.join(header)]

    # Merge two list => content file data send mail
    dataCreateFile = header + contents

    check_path = _create_file_mail(dataCreateFile, listFile, path)
    if FAIL in check_path:
        return check_path

    # Create TaskID.conts
    contentMail = CONTENT_MAIL % {'senders': request["senders"],
                                  'sendersMail': request["senders_mail"],
                                  'name': request["template_subject"], 'body': body}

    check_path = _create_file_mail(contentMail, contentFile, path)
    if FAIL in check_path:
        return check_path

    # Handle zip file
    with tarfile.open(tarGzDir, 'w:gz') as zip:
        zip.add(path, taskId)
        # If file exists, delete it
        if os.path.exists(path):
            shutil.rmtree(path)

    deliveryTime = datetime.strftime(datetime.now(tz.gettz('Asia/Tokyo')),
                                     '%Y%m%d %H:%M:%S')  # noqa E501

    payload = {'ClientID': MAIL_CLIENT_ID,
               'Type': TYPE_MAIL,
               'TaskID': taskId,
               'TaskType': f'{taskId}_{TYPE_MAIL}',
               'DeliveryTime': deliveryTime,
               'Interval': INTERVAL_MAIL,
               'TrackOpen': '1',
               'TrackClick': '1',
               'ToListNum': '1'}
    files = {'datafile': (tarGzFile, open(tarGzDir, 'rb'))}

    try:
        time.sleep(0.05)
        response = requests.post(f"{URL_MAIL}/v1/delivery/start", data=payload, files=files)
        # Delete file zip
        os.remove(tarGzDir)
    except Exception as err:
        return f"{FAIL} - call post fail - {err}"

    if response.status_code < 200 or response.status_code >= 300 \
            or response.json()['code'] < 200 or response.json()['code'] >= 300:
        return f"{FAIL} - response fail-  {response.text} - {response.json()}"

    return SUCCESS


def replace_body_message(text, channel: str):
    """ Replace body message convert to CM.com """
    regExp = re.findall(REG_EXP_PARAM_MESSAGE, text)
    # Convert body => body template cm.com
    for index, item in enumerate(regExp):
        regExp[index] = re.sub(r'[^\w]', '', to_camel_case(regExp[index]))
        if 'MAIL' == channel:
            text = text.replace(item, '{=%s=}' % to_camel_case(regExp[index]))

    return text, regExp


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def replace_url(body, isPersonalUrl=False):
    # findall() has been used
    # with valid conditions for urls in string
    # shortHex = uuid.uuid4().hex[:5]
    urls = re.findall(REG_EXP_PARAM_URL, body)

    if urls:
        for url in urls:
            href = url[2:-2]
            if href:
                if isPersonalUrl:
                    href = '<a href="{personal_url}' + href + '{/personal_url}" target="_blank">' + href + '</a>'  # noqa E501
                else:
                    href = '<a href="{click_url}' + href + '{/click_url}" target="_blank">' + href + '</a>'  # noqa E501
                body = body.replace(url, href)
    return body


def check_valid_email(email: str) -> Optional[bool]:
    # pass the regular expression
    # and the string in search() method
    if re.search(REGEX_MAIL, email):
        return True
    else:
        return False


def _create_file_mail(data, file_name, path) -> str:
    """メールファイルを作成"""

    # Create folder temporary
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as err:
        return f"{FAIL} - create folder - {err}"

    # Create File
    pathFile = f'{path}/{file_name}'
    with open(pathFile, 'w', encoding="utf-8") as file:
        if isinstance(data, str):
            file.write(data)
        else:
            for text in data:
                writer = '%s\r\n' % text
                file.write(writer)
    return path
