import time

from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, users_details_collection_name
from app.models.user_details import UserDeatailsInCreate, UserDeatailsInDB
from app.models.user import UserInUpdate


async def get_user_details(conn: AsyncIOMotorClient, user_id: str) -> UserDeatailsInDB:
    row = await conn[database_name][users_details_collection_name].find_one({"user_id": user_id})
    if row:
        return UserDeatailsInDB(**row)


async def create_user_details(
    conn: AsyncIOMotorClient,
    user_details: UserDeatailsInCreate,
    user_id: str
) -> UserDeatailsInDB:
    dbuser_details = UserDeatailsInDB(**user_details.dict())

    new_time = int(time.time())
    dbuser_details.created_at = new_time
    dbuser_details.updated_at = new_time
    dbuser_details.user_id = user_id

    await conn[database_name][users_details_collection_name].insert_one(dbuser_details.dict())

    return dbuser_details


async def update_user_details(
    conn: AsyncIOMotorClient,
    user: UserInUpdate,
    user_id: str
) -> UserDeatailsInDB:
    dbuser_details = await get_user_details(conn, user_id)

    FATS_PER_KG_IDEAL_WEIGHT = 1
    PROTEIN_CALORIE = 4
    FAT_CALORIE = 9
    CARBOHYDRATE_CALORIE = 4

    # Вспомогательные величины
    if user.sex == 1:
        dbuser_details.aditional_index.basic_metabolism_ratio = -161
    if user.sex == 2:
        dbuser_details.aditional_index.basic_metabolism_ratio = 5

    user_basic_metabolism_ratio = dbuser_details.aditional_index.basic_metabolism_ratio

    if user.activity == 1:
        dbuser_details.aditional_index.activity_ratio = 1.2
        dbuser_details.aditional_index.proteins_per_kg_ideal_weight = 1.5
    if user.activity == 2:
        dbuser_details.aditional_index.activity_ratio = 1.375
        dbuser_details.aditional_index.proteins_per_kg_ideal_weight = 1.7
    if user.activity == 3:
        dbuser_details.aditional_index.activity_ratio = 1.55
        dbuser_details.aditional_index.proteins_per_kg_ideal_weight = 2

    user_activity_ratio = dbuser_details.aditional_index.activity_ratio
    user_proteins_per_kg_ideal_weight = dbuser_details.aditional_index.proteins_per_kg_ideal_weight

    if user.target == 1:
        dbuser_details.aditional_index.goal_ratio = -400
    if user.target == 2:
        dbuser_details.aditional_index.goal_ratio = 0
    if user.target == 3:
        dbuser_details.aditional_index.goal_ratio = 400

    user_goal_ratio = dbuser_details.aditional_index.goal_ratio

    if user.age < 40:
        dbuser_details.aditional_index.ideal_weight = user.height - 110
    if user.age >= 40:
        dbuser_details.aditional_index.ideal_weight = user.height - 100

    user_ideal_weight = dbuser_details.aditional_index.ideal_weight

    # Вычисляемые и целевые показатели
    dbuser_details.calculated_targets.basic_metabolism = \
        user.weight * 10 + user.height * 6.25 - user.age * 5 + user_basic_metabolism_ratio

    user_basic_metabolism = dbuser_details.calculated_targets.basic_metabolism

    dbuser_details.calculated_targets.basic_calorie_intake = \
        user_basic_metabolism + user_activity_ratio

    user_basic_calorie_intake = dbuser_details.calculated_targets.basic_calorie_intake

    dbuser_details.calculated_targets.calories_to_goal = \
        user_basic_calorie_intake + user_goal_ratio

    user_calories_to_goal = dbuser_details.calculated_targets.calories_to_goal

    dbuser_details.calculated_targets.proteins_requirement = \
        user_ideal_weight * user_proteins_per_kg_ideal_weight

    user_proteins_requirement = dbuser_details.calculated_targets.proteins_requirement

    dbuser_details.calculated_targets.fats_requirement = \
        user_ideal_weight * FATS_PER_KG_IDEAL_WEIGHT

    user_fats_requirement = dbuser_details.calculated_targets.fats_requirement

    dbuser_details.calculated_targets.calories_from_proteins = \
        user_proteins_requirement * PROTEIN_CALORIE

    user_calories_from_proteins = dbuser_details.calculated_targets.calories_from_proteins

    dbuser_details.calculated_targets.calories_from_fats = \
        user_fats_requirement * FAT_CALORIE

    user_calories_from_fats = dbuser_details.calculated_targets.calories_from_fats

    dbuser_details.calculated_targets.calories_from_carbohydrates = \
        user_calories_to_goal - user_calories_from_proteins - user_calories_from_fats

    user_calories_from_carbohydrates = round(dbuser_details.calculated_targets.calories_from_carbohydrates, 1) 

    dbuser_details.calculated_targets.carbohydrates_requirement = \
        user_calories_from_carbohydrates / CARBOHYDRATE_CALORIE

    user_carbohydrates_requirement = dbuser_details.calculated_targets.carbohydrates_requirement

    # Расчет питания
    dbuser_details.calculated_foods.breakfast.fats_requirement = \
        round(user_fats_requirement * 0.2)

    dbuser_details.calculated_foods.lunch.proteins_requirement = \
        round(user_proteins_requirement * 0.3)

    dbuser_details.calculated_foods.lunch.fats_requirement = \
        round(user_fats_requirement * 0.2)

    dbuser_details.calculated_foods.lunch.carbohydrates_requirement = \
        round(user_carbohydrates_requirement * 0.3)

    dbuser_details.calculated_foods.snack.proteins_requirement = \
        round(user_proteins_requirement * 0.15)

    dbuser_details.calculated_foods.snack.fats_requirement = \
        round(user_fats_requirement * 0.3)

    dbuser_details.calculated_foods.snack.carbohydrates_requirement = \
        round(user_carbohydrates_requirement * 0.25)

    dbuser_details.calculated_foods.dinner.fats_requirement = \
        round(user_fats_requirement * 0.3)

    if user.sex == 1:
        dbuser_details.calculated_foods.breakfast.proteins_requirement = \
            round(user_proteins_requirement * 0.2)
        dbuser_details.calculated_foods.breakfast.carbohydrates_requirement = \
            round(user_carbohydrates_requirement * 0.35)
        dbuser_details.calculated_foods.dinner.proteins_requirement = \
            round(user_proteins_requirement * 0.35)
        dbuser_details.calculated_foods.dinner.carbohydrates_requirement = \
            round(user_carbohydrates_requirement * 0.1)

    if user.sex == 2:
        dbuser_details.calculated_foods.breakfast.proteins_requirement = \
            round(user_fats_requirement * 0.25)
        dbuser_details.calculated_foods.breakfast.carbohydrates_requirement = \
            round(user_carbohydrates_requirement * 0.3)
        dbuser_details.calculated_foods.dinner.proteins_requirement = \
            round(user_proteins_requirement * 0.3)
        dbuser_details.calculated_foods.dinner.carbohydrates_requirement = \
            round(user_carbohydrates_requirement * 0.15)

    dbuser_details.calculated_foods.breakfast.calories_requirement = \
        dbuser_details.calculated_foods.breakfast.proteins_requirement * PROTEIN_CALORIE + \
        dbuser_details.calculated_foods.breakfast.fats_requirement * FAT_CALORIE + \
        dbuser_details.calculated_foods.breakfast.carbohydrates_requirement * CARBOHYDRATE_CALORIE

    dbuser_details.calculated_foods.lunch.calories_requirement = \
        dbuser_details.calculated_foods.lunch.proteins_requirement * PROTEIN_CALORIE + \
        dbuser_details.calculated_foods.lunch.fats_requirement * FAT_CALORIE + \
        dbuser_details.calculated_foods.lunch.carbohydrates_requirement * CARBOHYDRATE_CALORIE

    dbuser_details.calculated_foods.snack.calories_requirement = \
        dbuser_details.calculated_foods.snack.proteins_requirement * PROTEIN_CALORIE + \
        dbuser_details.calculated_foods.snack.fats_requirement * FAT_CALORIE + \
        dbuser_details.calculated_foods.snack.carbohydrates_requirement * CARBOHYDRATE_CALORIE

    dbuser_details.calculated_foods.dinner.calories_requirement = \
        dbuser_details.calculated_foods.dinner.proteins_requirement * PROTEIN_CALORIE + \
        dbuser_details.calculated_foods.dinner.fats_requirement * FAT_CALORIE + \
        dbuser_details.calculated_foods.dinner.carbohydrates_requirement * CARBOHYDRATE_CALORIE

    new_time = int(time.time())
    dbuser_details.updated_at = new_time

    await conn[database_name][users_details_collection_name].update_one(
        {"user_id": user_id},
        {'$set': dbuser_details.dict()}
    )

    return dbuser_details
