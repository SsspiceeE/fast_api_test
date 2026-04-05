from pydantic import BaseModel, EmailStr

from typing import Optional


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    age: int
    full_name: Optional[str] = None


class UserCreateSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int


