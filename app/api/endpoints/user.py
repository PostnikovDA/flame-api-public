from fastapi import APIRouter, Depends, Body

from app.models.user import UserInResponse, User, UserInUpdate
from app.core.jwt import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.crud.user import update_user

router = APIRouter()


@router.get('/user', response_model=UserInResponse, tags=['users'])
async def return_current_user(user: User = Depends(get_current_user_authorizer)):
    return UserInResponse(profile=user)


@router.put('/user', response_model=UserInResponse, tags=['users'])
async def update_current_user(
    user: UserInUpdate = Body(..., embed=True),
    curren_user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
):
    dbuser = await update_user(db, curren_user.firebase_id, user)
    return UserInResponse(profile=User(**dbuser.dict()))
