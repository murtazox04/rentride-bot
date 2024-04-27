from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    access: str
    refresh: str


class User(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id')
    username: str
    hashed_password: str
    tokens: TokenModel

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
