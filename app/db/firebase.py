import firebase_admin
from firebase_admin import credentials, auth
from pydantic import BaseModel
from fastapi import HTTPException, status

from app.core.config import FIREBASE_CONFIG


cred = credentials.Certificate(FIREBASE_CONFIG)
firebase_admin.initialize_app(cred)


def get_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
        )
    return decoded_token


class FireBase(BaseModel):
    firebase_token: str
