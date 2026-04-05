from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import UserResponseSchema, UserCreateSchema
from app.core.dep import get_db
from app.models.user import User
from app.utils.password_hash import hash_password

router = APIRouter(prefix='/users')


@router.get('/user', response_model=List[UserResponseSchema])
async def get_users(
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User))
    return result.scalars().all()


@router.get('/user/{pk}', response_model=UserResponseSchema)
async def get_user(
        pk: int,
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.id == pk)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@router.post('/user', status_code=201, response_model=UserResponseSchema)
async def add_user(
        user_json: UserCreateSchema,
        db: AsyncSession = Depends(get_db),
):
    user_data = user_json.model_dump()
    user_data['password_hash'] = hash_password(user_data['password'])
    del user_data['password']
    new_user = User(**user_data)
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user
