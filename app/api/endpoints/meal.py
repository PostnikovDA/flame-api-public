from fastapi import APIRouter, Depends, Body, HTTPException, status

from app.models.user import User
from app.models.meal import MealList, MealInDB, MealInResponse
from app.core.jwt import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.crud.meal import get_meals, create_meal

router = APIRouter()


@router.get('/meal', response_model=MealList, tags=['foods'])
async def return_all_meals(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
):

    dbmeals = await get_meals(db)
    return MealList(meals=[meal for meal in dbmeals])


@router.post(
    '/meal',
    response_model=MealInResponse,
    tags=['foods']
)
async def add_meal(
    user: User = Depends(get_current_user_authorizer),
    meal: MealInDB = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_mongodb)
):
    dbmeal = await create_meal(db, meal)
    return MealInResponse(info=dbmeal)
