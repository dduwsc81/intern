class Constants:
    TAX_RATE_DIV = 24
    # Delete flag: Normal
    DEL_FLG_NORMAL = 0
    # Delete flag: Delete
    DEL_FLG_DELETE = 1
    SHOW_TOTAL = 1
    SHOW_ONE = 0
    TIME_END_DATE = " 23:59:59"
    PURCHASE_CLOSE = 2
    BUY = 1
    SELL = 2
    RESET_CHAT_FLG = 1
    CHATTING_FLG = 2
    ENABLE = 1
    DISABLE = 0
    INDIVIDUAL = 1
    CORPORATE = [2, 3]
    HAS_SINGLE_VALUE = 1
    MEMO_CREATE_AT = 1
    MEMO_EDITOR = 2
    SORT_ASC = 1
    SORT_DESC = -1

    class ServiceCode:
        MARKET_FEE = "P002"

    # TODO: hard code admin_id
    ADMIN_ID = 88888

    CONFIG_MAIL = {
        "DIV_MAIL": 9,
        "SENDER": "send_customer_mail_sender",
        "SENDER_EMAIL": "send_customer_mail_sender_mail",
        "SENDER_EMAIL_LOTAS": "send_customer_mail_sender_mail_lotas",
        "SENDER_LOTAS": "send_customer_mail_sender_lotas",
        "ADMIN_BASE_URL": "send_customer_mail_admin_base_url",
    }

    class CarStatus:
        HYPEN = 0
        UNDER_EXHIBITION = 1
        UNDER_NEGOTIATION = 2
        CONTRACTED = 3
        CLOSE = 4
        APPLYING = 5

    class SaleStatus:
        UNDER_EXHIBITION = 1
        SALE_EXPIRED = 2
        STOP_SALE = 3
        UNDER_NEGOTIATION = 4
        CONTRACTED = 5
        CLOSE = 6

    class HttpMethod:
        GET = "get"
        POST = "post"
        PUT = "put"
        DELETE = "delete"

    CONFIG_RESERVE_URL = {
        "DIV_RESERVE": "13",
        "DIV_CATALOG": "4"
    }

    class Sort:
        CAR_STATUS = "car_status"

    CAR_STATUS_REGISTERED = (CarStatus.UNDER_EXHIBITION,
                             CarStatus.UNDER_NEGOTIATION,
                             CarStatus.CONTRACTED,
                             CarStatus.CLOSE)


Const = Constants()
