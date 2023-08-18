
from typing import List
from fastapi import HTTPException, status
import uuid

from app.db.mongodb import AsyncIOMotorClient
from app.models.food import FoodInDB, FoodInUpdate, FoodInCreate
from app.models.food_types import FoodTypesInDB
from app.core.config import database_name, foods_collection_name, foods_types_collection_name


async def get_food_by_id(conn: AsyncIOMotorClient, id: str) -> FoodInDB:
    row = await conn[database_name][foods_collection_name].find_one({"id": id})
    if row:
        return FoodInDB(**row)


async def get_foods_by_group_id(
    conn: AsyncIOMotorClient,
    group_id: int,
    skip: int,
    limit: int
) -> FoodInDB:
    rows = conn[database_name][foods_collection_name].find(
        {'group_id': group_id}
    ).skip(skip).limit(limit)
    foods_by_type = []
    async for row in rows:
        foods_by_type.append(FoodInDB(**row))
    return foods_by_type


async def get_food_types(conn: AsyncIOMotorClient) -> List[FoodTypesInDB]:
    rows = conn[database_name][foods_types_collection_name].find()
    food_types = []
    async for row in rows:
        food_types.append(FoodTypesInDB(**row))
    return food_types


async def get_food_by_title(conn: AsyncIOMotorClient, title: str) -> FoodInDB:
    row = await conn[database_name][foods_collection_name].find_one({"title": title})
    if row:
        return FoodInDB(**row)


async def create_food(conn: AsyncIOMotorClient, food: FoodInCreate) -> FoodInDB:
    dbfood = await get_food_by_title(conn, food.title)
    if dbfood:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Entity already exist.'
        )

    dbfood = FoodInDB(**food.dict())
    dbfood.id = str(uuid.uuid4().hex)
    await conn[database_name][foods_collection_name].insert_one(dbfood.dict())

    return dbfood


async def update_food(conn: AsyncIOMotorClient, food: FoodInUpdate, id: str) -> FoodInDB:
    dbfood = await get_food_by_id(conn, id)

    if not dbfood:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Food by id: {id} not found'
        )

    dbfood.image = food.image or dbfood.image
    dbfood.group_id = food.group_id or dbfood.group_id
    dbfood.title = food.title or dbfood.title
    dbfood.carbohydrates = food.carbohydrates or dbfood.carbohydrates
    dbfood.fats = food.fats or dbfood.fats
    dbfood.proteins = food.proteins or dbfood.proteins
    dbfood.calories = food.calories or dbfood.calories

    await conn[database_name][foods_collection_name].update_one(
        {"id": id},
        {'$set': dbfood.dict()}
    )

    return dbfood


async def delete_food(conn: AsyncIOMotorClient, id: str) -> FoodInDB:
    dbfood = await get_food_by_id(conn, id)

    if not dbfood:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Food by id: {id} not found'
        )

    await conn[database_name][foods_collection_name].delete_one({'id': id})
