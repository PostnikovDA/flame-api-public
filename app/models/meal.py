from pydantic import BaseModel
from typing import List, Dict, Optional


class MealBase(BaseModel):
    title: str
    meal_id: Optional[int]


class MealInDB(MealBase):
    pass


class Meal(MealBase):
    pass


class MealInResponse(BaseModel):
    info: Meal


class MealInCreate(MealBase):
    pass


class MealList(BaseModel):
    meals: List[Dict] = []
