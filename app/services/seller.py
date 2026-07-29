from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..api.schemas.seller import SellerCreate
from ..database.models import Seller
from passlib.context import CryptContext

pass_ctx = CryptContext(schemes=["bcrypt"])

class SellerService:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def add(self, credentials:SellerCreate) -> Seller:
        new_seller = Seller(
            **credentials.model_dump(exclude="password"),
            password_hash=pass_ctx.hash(credentials.password)
        )
        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh()
        return new_seller

    async def token(self, email:str, password:str) -> str:
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        if result is None or not pass_ctx.verify(password, Seller.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Email or password does not match")

