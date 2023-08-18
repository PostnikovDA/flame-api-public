from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import Optional
from datetime import date, datetime

from app.models.dbmodel import DBModelMixin
from app.core.security import generate_salt, get_password_hash, verify_password


class BaseUserMixin(BaseModel):
    @validator('birthday', pre=True, check_fields=False)
    def _parse_birthday(cls, user_date):
        if isinstance(user_date, str):
            return datetime.strptime(
                user_date,
                "%d-%m-%Y"
            ).date()
        return user_date


class UserBase(BaseUserMixin, BaseModel):
    username: str = ''
    phone_number: Optional[str] = ''
    permission: str = 'user:read'
    birthday: date = None
    sex: Optional[int]
    age: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    target: Optional[int]
    daily_calorie_intake: Optional[int]
    email: EmailStr = None
    image: Optional[HttpUrl] = None
    activity: int = None
    payment_status: bool = False


class UserInDB(DBModelMixin, UserBase):
    firebase_id: Optional[str]
    sign_in_provider: Optional[str]
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(UserBase):
    firebase_id: Optional[str]
    user_id: Optional[str]


class UserInResponse(BaseModel):
    profile: User


class UserInLogin(BaseModel):
    access_token: str


class UserInLoginViaEmail(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserBase):
    firebase_id: Optional[str]
    sign_in_provider: Optional[str]
    password: Optional[str]


class UserInUpdate(BaseUserMixin, BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    sex: Optional[int] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    target: Optional[int] = None
    email: Optional[EmailStr] = None
    image: Optional[HttpUrl] = None
    activity: Optional[int] = None
    payment_status: Optional[bool] = None
