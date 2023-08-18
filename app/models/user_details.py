from pydantic import BaseModel, Field
from typing import List

from app.models.dbmodel import DBModelMixin


class AditionalIndex(BaseModel):
    basic_metabolism_ratio: int = None
    activity_ratio: float = None
    goal_ratio: int = None
    proteins_per_kg_ideal_weight: float = None
    ideal_weight: int = None


class CalculatedTargets(BaseModel):
    basic_metabolism: float = None
    basic_calorie_intake: float = None
    calories_to_goal: float = None
    proteins_requirement: float = None
    fats_requirement: int = None
    carbohydrates_requirement: float = None
    calories_from_proteins: float = None
    calories_from_fats: float = None
    calories_from_carbohydrates: float = None


class BaseOrganicMatter(BaseModel):
    proteins_requirement: int = None
    fats_requirement: int = None
    carbohydrates_requirement: int = None
    calories_requirement: int = None


class Breakfast(BaseOrganicMatter):
    pass


class Lunch(BaseOrganicMatter):
    pass


class Snack(BaseOrganicMatter):
    pass


class Dinner(BaseOrganicMatter):
    pass


class CalculatedFoods(BaseModel):
    breakfast: Breakfast = {}
    lunch: Lunch = {}
    snack: Snack = {}
    dinner: Dinner = {}


class UserDeatailsBase(BaseModel):
    aditional_index: AditionalIndex = {}
    calculated_targets: CalculatedTargets = {}
    calculated_foods: CalculatedFoods = {}
    favorite_food: List[str] = []


class UserDeatails(UserDeatailsBase):
    pass


class UserDeatailsInDB(DBModelMixin, UserDeatailsBase):
    pass


class UserDeatailsInCreate(UserDeatailsBase):
    pass


class UserDeatailsInResponse(BaseModel):
    user_details: UserDeatails
