
from typing import List
from app.db.mongodb import AsyncIOMotorClient
from app.models.meal import MealInDB, MealInCreate
from fastapi import HTTPException, status
from app.core.config import database_name, meals_collection_name


async def get_meal_by_id(conn: AsyncIOMotorClient, id: int) -> MealInDB:
    row = await conn[database_name][meals_collection_name].find_one({"meal_id": id})
    if row:
        return MealInDB(**row)


async def get_meal_by_title(conn: AsyncIOMotorClient, title: str) -> MealInDB:
    row = await conn[database_name][meals_collection_name].find_one({"title": title})
    if row:
        return MealInDB(**row)


async def get_meals(conn: AsyncIOMotorClient) -> List[MealInDB]:
    rows = conn[database_name][meals_collection_name].find()
    meals = []
    async for row in rows:
        meals.append(MealInDB(**row))
    return meals


async def create_meal(conn: AsyncIOMotorClient, meal: MealInCreate) -> MealInDB:
    dbmeal = await get_meal_by_title(conn, meal.title)
    if dbmeal:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Entity already exist.'
        )

    dbmeals = await get_meals(conn)
    meals_id_list = [meal.meal_id for meal in dbmeals]
    if not meals_id_list:
        meals_id_list.append(0)
    meals_id_list.sort()
    dbmeal = MealInDB(**meal.dict())
    dbmeal.meal_id = max(meals_id_list) + 1
    await conn[database_name][meals_collection_name].insert_one(dbmeal.dict())

    return dbmeal
