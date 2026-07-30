from datetime import timedelta

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import generate_access_token

from ..api.schemas.seller import SellerCreate
from ..database.models import Seller

pass_ctx = CryptContext(schemes=["argon2", "bcrypt"])

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
        await self.session.refresh(new_seller)
        return new_seller

    async def token(self, email:str, password:str) -> str:
        query = await self.session.execute(select(Seller).where(Seller.email == email))
        seller = query.scalar()

        if seller is None or not pass_ctx.verify(password, seller.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = generate_access_token(data={
            "user":{
                "name": seller.name,
                "id": str(seller.id)
            }
        }, expiry=timedelta(days=7))

        return token

    

        


