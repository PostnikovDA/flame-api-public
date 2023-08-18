import time
import uuid
from dateutil.relativedelta import relativedelta
from datetime import date
from fastapi import HTTPException, status
from pydantic import EmailStr
from typing import Optional

from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, users_collection_name
from app.models.user import UserInCreate, UserInDB, UserInUpdate
from app.models.user_details import UserDeatailsInCreate
from app.crud.user_details import get_user_details, create_user_details, update_user_details


async def get_user(conn: AsyncIOMotorClient, firebase_id: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"firebase_id": firebase_id})
    if row:
        return UserInDB(**row)


async def get_user_by_username(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDB(**row)


async def check_free_username_and_email(
        conn: AsyncIOMotorClient, username: Optional[str] = None, email: Optional[EmailStr] = None
):
    if username:
        user_by_username = await get_user_by_username(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict())

    if user.password:
        dbuser.change_password(user.password)

    new_time = int(time.time())
    dbuser.created_at = new_time
    dbuser.updated_at = new_time
    dbuser.user_id = str(uuid.uuid4().hex)
    await conn[database_name][users_collection_name].insert_one(dbuser.dict())

    dbuser_details = await get_user_details(conn, dbuser.user_id)
    if not dbuser_details:
        await create_user_details(
            conn,
            user_details=UserDeatailsInCreate(),
            user_id=dbuser.user_id
        )

    return dbuser


async def update_user(conn: AsyncIOMotorClient, firebase_id: str, user: UserInUpdate) -> UserInDB:
    dbuser = await get_user(conn, firebase_id)

    dbuser.username = user.username or dbuser.username
    dbuser.phone_number = user.phone_number or dbuser.phone_number
    dbuser.email = user.email or dbuser.email
    dbuser.image = user.image or dbuser.image

    if user.activity is None and dbuser.activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Field activity is empty in db. Plese set it in body.'
        )
    dbuser.activity = user.activity or dbuser.activity

    if user.birthday is None and dbuser.birthday is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Field birthday is empty in db. Plese set it in body.'
        )
    else:
        dbuser.birthday = user.birthday or dbuser.birthday

    if user.sex is None and dbuser.sex is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Field sex is empty in db. Plese set it in body.'
        )
    else:
        dbuser.sex = user.sex or dbuser.sex

    if user.height is None and dbuser.height is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Field height is empty in db. Plese set it in body.'
        )
    else:
        dbuser.height = user.height or dbuser.height

    if user.weight is None and dbuser.weight is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Field weight is empty in db. Plese set it in body.'
        )
    else:
        dbuser.weight = user.weight or dbuser.weight

    if user.target is None and dbuser.target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Field target is empty in db. Plese set it in body.'
        )
    else:
        dbuser.target = user.target or dbuser.target

    dbuser.age = int(relativedelta(date.today(), dbuser.birthday).years)
    user_date = dbuser.birthday
    dbuser.birthday = '-'.join(str(d) for d in (user_date.day, user_date.month, user_date.year))

    new_time = int(time.time())
    dbuser.updated_at = new_time

    await conn[database_name][users_collection_name].update_one(
        {"firebase_id": dbuser.firebase_id},
        {'$set': dbuser.dict()}
    )

    await update_user_details(conn, user=dbuser, user_id=dbuser.user_id)

    return dbuser
