from fastapi import APIRouter, Depends, Path

from app.models.user import User
from app.core.jwt import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.models.user_details import UserDeatailsInResponse, UserDeatails
from app.crud.user_details import get_user_details

router = APIRouter()


@router.get('/user_details/{user_id}', response_model=UserDeatailsInResponse, tags=['users'])
async def return_user_details_by_user_id(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
    user_id: str = Path(...),
):
    dbuser_details = await get_user_details(db, user_id=user_id)
    return UserDeatailsInResponse(user_details=UserDeatails(**dbuser_details.dict()))
