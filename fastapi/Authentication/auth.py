import time
from typing import Dict

import jwt
from decouple import config

from passlib.context import CryptContext


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string
def signJWT(user_id: str ) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def get_user_data(token: str):
    decoded_token = decodeJWT(token)
    print(decoded_token)
    user_id = decoded_token.get("user_id")
    expires = decoded_token.get("expires")
    if user_id:
        user_data = {
            "email": user_id,
            "expires": expires
        }
        return user_data
    else:
        return None

# if __name__ == '__main__':
#     print(get_user_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoicG9vc2EucEBub3J0aGVhc3Rlcm4uZWR1IiwiZXhwaXJlcyI6MTY4MjAyNzEyOC4yNTk1MzF9.fh3STfeHo4bEQcD3TXM-jW7-be-U8Ck0QkYcQqL92is'))