from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserCreateResponse(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)

class UserInfoResponse(BaseModel):
    id: int
    username: str
    role: str

class UserCreds(BaseModel):
    username: str
    password: str

class ItemSchema(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)
