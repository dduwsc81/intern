from jose import jwt
from requests import Request
import re
from app.core.config import settings
from urllib.parse import urlparse

COGNITO_ISS_PATTERN = r'^https://cognito-idp.[0-9a-zA-Z_-]+.amazonaws.com/([0-9a-zA-Z_-]+)$'
HEALTH_CHECK_PATH = settings.API_V1_STR + '/health_check'
ADMIN_ROLE = '32'


class AdminMiddleware():

    def check_role(self, request: Request):
        self.pattern = re.compile(COGNITO_ISS_PATTERN)

        path = urlparse(str(request.url)).path
        if path != HEALTH_CHECK_PATH:
            # check role
            decoded_str = self.get_auth(request)
            return 1 if decoded_str and decoded_str['role_name'] == ADMIN_ROLE else None
        return 1

    def decode(self, token):
        try:
            claims = jwt.get_unverified_claims(token)
            match = self.pattern.match(claims.get('iss'))
            if match:
                userpoolId = match.group(1)
            claims['userpoolId'] = userpoolId
            return claims
        except BaseException:
            return None

    def get_token(self, request):
        try:
            _type, token = request.headers['Authorization'].split(" ")
            if _type.lower() != "bearer":
                return None
            return token
        except BaseException:
            return None

    def get_auth(self, request):
        token = self.get_token(request)
        if not token:
            return None
        decoded = self.decode(token)
        if not decoded:
            return None
        return decoded
