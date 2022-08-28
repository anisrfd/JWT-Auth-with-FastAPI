import time
from typing import Dict
import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def signin_jwt(user_id: str) -> Dict[str, str]:
    """
    Takes user_id and used for signing
    the JWT string and returns token

    :param user_id: str object
    :return: dict object
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "access_token": token
    }


def decode_jwt(token: str) -> dict:
    """
    Takes token and decode it

    :param token: Request object
    :return: dict object
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
