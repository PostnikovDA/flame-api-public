from pydantic import BaseModel, HttpUrl

from typing import List, Dict, Optional


class FoodBase(BaseModel):
    image: HttpUrl = None
    group_id: int = None
    title: str = ''
    carbohydrates: float = None
    fats: float = None
    proteins: float = None
    calories: int = None


class FoodInDB(FoodBase):
    id: str = ''


class Food(FoodBase):
    pass


class FoodInResponse(BaseModel):
    info: Food


class FoodList(BaseModel):
    products: List[Dict] = []


class FoodInCreate(FoodBase):
    pass


class FoodInUpdate(BaseModel):
    image: Optional[HttpUrl] = None
    group_id: Optional[int] = None
    title: Optional[str] = ''
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    proteins: Optional[float] = None
    calories: Optional[int] = None
