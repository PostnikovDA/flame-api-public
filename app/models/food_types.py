from pydantic import BaseModel

from typing import Dict, List


class FoodTypesBase(BaseModel):
    group_id: int = None
    title: str = ''


class FoodTypes(FoodTypesBase):
    pass


class FoodTypesInDB(FoodTypes):
    pass


class FoodTypesList(BaseModel):
    types: List[Dict] = []
