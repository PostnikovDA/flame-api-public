from pydantic import BaseModel


class TokenPayload(BaseModel):
    firebase_id: str = ''
