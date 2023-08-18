from fastapi import APIRouter, Depends, Body, Query

from app.models.user import User
from app.models.dish import DishInResponse, DishInDB, DishList
from app.core.jwt import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.crud.dish import create_dish, get_dishes_by_meal_id, get_all_dishes

router = APIRouter()


@router.get('/dish', response_model=DishList, tags=['foods'])
async def return_dishes_by_meal_id(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
    meal_id: int = Query(...)
):

    dbdishes = await get_dishes_by_meal_id(db, meal_id)
    return DishList(dishes=[dish for dish in dbdishes])


@router.get('/dish/all', response_model=DishList, tags=['foods'])
async def return_all_dishes(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb)
):

    dbdishes = await get_all_dishes(db)
    return DishList(dishes=[dish for dish in dbdishes])


@router.post(
    '/dish',
    response_model=DishInResponse,
    tags=['foods']
)
async def add_dish(
    user: User = Depends(get_current_user_authorizer),
    dish: DishInDB = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_mongodb)
):
    dbdish = await create_dish(db, dish)
    return DishInResponse(info=dbdish)
