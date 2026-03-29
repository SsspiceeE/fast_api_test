from pydantic import BaseModel, EmailStr

from typing import Optional


class BaseUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    age: int
    full_name: Optional[str] = None


class ModelUser(BaseUser):
    id: int

