from fastapi import APIRouter

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.user import router as user_router
from app.api.endpoints.user_details import router as user_details_router
from app.api.endpoints.food import router as food_router
from app.api.endpoints.meal import router as meal_router
from app.api.endpoints.dish import router as dish_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(food_router)
router.include_router(user_details_router)
router.include_router(meal_router)
router.include_router(dish_router)
