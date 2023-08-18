from fastapi import APIRouter, Depends, Query, Path
from fastapi.param_functions import Body

from app.models.user import User
from app.models.food_types import FoodTypesList
from app.models.food import FoodInDB, FoodList, FoodInResponse, FoodInUpdate
from app.core.jwt import get_current_user_authorizer
from app.db.mongodb import AsyncIOMotorClient, get_mongodb
from app.crud.food import get_food_types, get_foods_by_group_id, get_food_by_id, update_food, create_food, delete_food

router = APIRouter()


@router.get('/food/types', response_model=FoodTypesList, tags=['foods'])
async def return_all_food_types(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
):

    dbfood_types = await get_food_types(db)
    return FoodTypesList(types=[food_type for food_type in dbfood_types])


@router.get('/food', response_model=FoodList, tags=['foods'])
async def return_foods_by_group_id(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
    group_id: int = Query(...),
    skip: int = Query(0, le=100),
    limit: int = Query(100, le=1000)
):
    dbfoods = await get_foods_by_group_id(db, group_id, skip, limit)
    return FoodList(products=[food for food in dbfoods])


@router.get('/food/{id}', response_model=FoodInResponse, tags=['foods'])
async def return_food_by_id(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
    id: str = Path(...)
):
    dbfood = await get_food_by_id(db, id)
    return FoodInResponse(info=dbfood)


@router.post(
    '/food',
    response_model=FoodInResponse,
    tags=['foods']
)
async def add_food(
    user: User = Depends(get_current_user_authorizer),
    food: FoodInDB = Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_mongodb)
):
    dbfood = await create_food(db, food)
    return FoodInResponse(info=dbfood)


@router.put('/food/{id}', response_model=FoodInResponse, tags=['foods'])
async def update_food_by_id(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
    food: FoodInUpdate = Body(..., embed=True),
    id: str = Path(...)
):
    dbfood = await update_food(db, food, id)
    return FoodInResponse(info=dbfood)


@router.delete('/food/{id}', tags=['foods'])
async def delete_food_by_id(
    user: User = Depends(get_current_user_authorizer),
    db: AsyncIOMotorClient = Depends(get_mongodb),
    id: str = Path(...)
):
    await delete_food(db, id)
    return {"msg": "ok"}
