from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.crud.user import get_user, get_user_by_email
from app.models.user import User
from app.models.token import TokenPayload


SECRET_KEY = 'dKxoLp0w0dy4n2sR6RS5gVYzun6MQEsISREdGVxjthvCVx55NFxP4aephL4mJsk'
ALGORITHM = 'HS256'


def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(' ')
    if token_prefix != 'Bearer':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization type'
        )

    return token


async def get_current_user_authorizer(
    *, db: AsyncIOMotorClient = Depends(get_mongodb), token: str = Depends(_get_authorization_token)
) -> User:
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    if token_data.firebase_id:
        dbuser = await get_user(db, token_data.firebase_id)
        if not dbuser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif token_data.email:
        dbuser = await get_user_by_email(db, token_data.email)
        if not dbuser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unprocessable entity")

    user = User(**dbuser.dict())
    return user


def create_access_token(*, data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt
