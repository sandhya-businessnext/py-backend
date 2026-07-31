from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user import UserService

from ..api.schemas.seller import SellerCreate
from ..database.models import Seller



class SellerService(UserService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, Seller)
        self.session = session

    async def add(self, credentials:SellerCreate) -> Seller:
        return await self._add_user(credentials)

    async def token(self, email:str, password:str) -> str:
        return await self._get_access_token(email, password)

    

        


