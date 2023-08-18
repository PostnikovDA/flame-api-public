from typing import Optional
from pydantic import BaseModel


class DateTimeModelMixin(BaseModel):
    created_at: Optional[int] = None
    updated_at: Optional[int] = None


class DBModelMixin(DateTimeModelMixin):
    user_id: str = ''
