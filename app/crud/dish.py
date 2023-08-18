from fastapi import HTTPException, status
from typing import List
import uuid

from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, dishes_collection_name
from app.models.dish import DishInDB, DishInCreate


async def get_dish_by_id(conn: AsyncIOMotorClient, id: int) -> DishInDB:
    row = await conn[database_name][dishes_collection_name].find_one({"id": id})
    if row:
        return DishInDB(**row)


async def get_dish_by_title(conn: AsyncIOMotorClient, title: str) -> DishInDB:
    row = await conn[database_name][dishes_collection_name].find_one({"title": title})
    if row:
        return DishInDB(**row)


async def get_dishes_by_meal_id(conn: AsyncIOMotorClient, meal_id: int) -> List[DishInDB]:
    rows = conn[database_name][dishes_collection_name].find({"meal_id": meal_id})
    dishes = []
    async for row in rows:
        dishes.append(DishInDB(**row))
    return dishes


async def get_all_dishes(conn: AsyncIOMotorClient) -> List[DishInDB]:
    rows = conn[database_name][dishes_collection_name].find({})
    dishes = []
    async for row in rows:
        dishes.append(DishInDB(**row))
    return dishes


async def create_dish(conn: AsyncIOMotorClient, dish: DishInCreate) -> DishInDB:
    dbdish = await get_dish_by_title(conn, dish.title)
    if dbdish:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Entity already exist.'
        )

    dbdish = DishInDB(**dish.dict())
    dbdish.id = str(uuid.uuid4().hex)
    await conn[database_name][dishes_collection_name].insert_one(dbdish.dict())

    return dbdish
