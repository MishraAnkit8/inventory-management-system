# inventory/utils.py
import jwt
import datetime
from django.conf import settings

def generate_access_token(user_id):
    """Generate JWT access token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    print(f"JWT Access Token generated for user {user_id}")
    return token

def generate_refresh_token(user_id):
    """Generate JWT refresh token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    print(f"JWT Refresh Token generated for user {user_id}")
    return token

def decode_token(token):
    """Decode a JWT token"""
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        print(f"Decoded JWT Token: {decoded}")
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')
