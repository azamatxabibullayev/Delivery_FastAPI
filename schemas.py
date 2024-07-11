from pydantic import BaseModel
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator


class SignupModel(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    is_staff: bool


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class ProductSchema(BaseModel):
    id: Optional[int]
    name: str
    price: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Example Product",
                "price": 100,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = "a12gd5678d48823cf1cef29abdb691ea31018024ddbg1cb4c794237d16a92ce5"
