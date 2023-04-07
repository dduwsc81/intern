import logging
from datetime import datetime, timedelta
from pathlib import Path
import math
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt

from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.m_system_param import MSystemParam
from app.constants import Const
import os

DIV_LOTAS = 8
ALGORITHM = "HS256"
SECRET_KEY_SURVEY_URL = str(os.environ["QUESTIONNAIRE_JWT_SECRET_2"])

def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def get_keys_from_values(dict_base : dict, values: list):
    # list out keys and values separately
    key_list = list(dict_base.keys())
    val_list = list(dict_base.values())

    key_result = []
    for value in values:
        position = val_list.index(value)
        key_result.append(key_list[position])

    return key_result


def round_number(number: int):
    temp = number % 1000
    if temp >= 500:
        return (number // 1000 + 1) * 1000
    else:
        return (number // 1000) * 1000


def round_decimal(input):
    if (float(input) % 1) >= 0.5:
        result = math.ceil(input)
    else:
        result = round(input)
    return result


def create_request_send_mail(params, mail_address, sender, sender_mail, mail_format):
    list_data = []
    obj_data = {
        "email": mail_address,
        "params": params
    }
    list_data.append(obj_data)

    req = {
        "channels": "MAIL",
        "senders": sender,
        "senders_mail": sender_mail,
        "template_subject": mail_format["title"] if mail_format else "",
        "body": mail_format["content"] if mail_format else "",
        "data": list_data
    }

    return req


def check_lotas_tech(db: Session, company_code):
    result = (
            db.query(MSystemParam)
            .filter(
                    MSystemParam.div == DIV_LOTAS,
                    MSystemParam.desc1 == company_code,
                    MSystemParam.delete_flag == Const.DEL_FLG_NORMAL,

            )
            .all()
        )
    if result:
        return True
    else:
        return False


# Func encode token
def encode_token(encode_data) -> str:
    # encoded by jwt
    try:
        encoded = jwt.encode(encode_data, SECRET_KEY_SURVEY_URL, algorithm=ALGORITHM)
        return encoded
    except jwt.JWTError:
        return ""
