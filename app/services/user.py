# _add_user, getbyemail, generate access token

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database.models import User
from app.core.utils import generate_access_token, hash_password, verify_password

from .base import BaseService

class UserService(BaseService):
    def __init__(self, model:User, session:AsyncSession):
        self.session = session
        self.model = model

    async def _add_user(self, data:dict):
        new_user = self.model(
            **data.model_dump(exclude={"password"}),
            password_hash=hash_password(data.password)
        )
        return await self._add(new_user)

    async def _get_by_email(self, email:str) -> User | None:
        return await self.session.scalar(select(self.model).where(self.model.email == email))

    async def _get_access_token(self, email:str, password:str) -> str:
        user = await self._get_by_email(email)

        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email or password is incorrect")
        token = generate_access_token({
            "user":{
                "name":user.name,
                "id":str(user.id)
            }
        })
        return token

    async def _update_password(self, email:str, old_password:str, new_password:str):
        user = await self._get_by_email(email)
        if user is None or not verify_password(old_password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password")

        new_user = await self._update(entity={
            **user,
            "password_hash":hash_password(new_password)
            
        })
        await self.session.commit()
        await self.session.refresh(new_user)

    async def _get_user_by_id(self, id:str) -> User | None:
        return await self.session.get(self.model, id)

    async def _delete_user(self, email:str) -> None:
        user = await self._get_by_email(email)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        await self._delete(user)




    