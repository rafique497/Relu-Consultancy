"""
 utility file
"""
# django import
import jwt
from datetime import datetime
from django.conf import settings
from calendar import timegm
from uuid import uuid4


def generate_jwt_token(token_type: str, now_time: datetime, data: dict = dict, ):
    """
    used to generate jwt token
    """
    if type(data) == type:
        data = {}
    data.update({
        'token_type': token_type,
        'iss': 'your_site_url',
        'iat': datetime.utcnow(),
        'jti': uuid4().hex,
    })
    if token_type == 'refresh':
        exp = now_time + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    else:
        exp = now_time + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

    data.update({
        "exp": timegm(exp.utctimetuple())
    })
    token = jwt.encode(payload=data, key=settings.SIMPLE_JWT['SIGNING_KEY'],
                       algorithm=settings.SIMPLE_JWT['ALGORITHM'])

    return token


def get_token(data: dict = dict):
    """get token"""
    now_time = datetime.utcnow()
    access = generate_jwt_token('access', now_time, data)
    refresh = generate_jwt_token('refresh', now_time, data)

    return {
        'access': access,
        'refresh': refresh
    }


