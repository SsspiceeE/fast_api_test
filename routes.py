from typing import List

from fastapi import APIRouter

from schemas import BaseUser, ModelUser


router = APIRouter(prefix='/api')

users = []


@router.post('/user/', status_code=201, response_model=ModelUser)
async def add_user(user: BaseUser):
    new_id = len(users) + 1
    new_user = ModelUser(id=new_id, **user.model_dump())
    users.append(new_user)
    return new_user


@router.get('/user/', response_model=List[ModelUser])
async def get_users():
    return users


@router.get('/user/{pk}', response_model=ModelUser)
async def get_user(pk: int):
    return users[pk - 1]