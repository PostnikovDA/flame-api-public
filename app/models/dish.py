from pydantic import BaseModel
from typing import List, Dict, Optional


class DishBase(BaseModel):
    title: str
    meal_id: int
    foods: List[str]


class DishInDB(DishBase):
    id: str = ''


class Dish(DishBase):
    pass


class DishInResponse(BaseModel):
    info: Dish


class DishList(BaseModel):
    dishes: List[Dict] = []


class DishInCreate(DishBase):
    pass


class DishInUpdate(BaseModel):
    title: Optional[str] = ''
    meal_id: Optional[int] = None
    foods: Optional[List[str]] = []
