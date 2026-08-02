


from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import any_, select

from app.api.schemas.delivery_partner import PartnerCreate
from app.database.models import DeliveryPartner
from app.services.user import UserService


class DeliveryPartnerService(UserService):

    def __init__(self, session:AsyncSession):
        super().__init__(session, DeliveryPartner)
        self.session = session

    async def add(self, credentials:PartnerCreate) -> DeliveryPartner:
        return self._add(credentials)

    async def token(self, email:str, password:str) -> str:
        return self._token(email, password)

    async def get_partners_by_zipcode(self, zipcode:int) -> list[DeliveryPartner]:
       return (await self.session.scalars(select(DeliveryPartner).where(zipcode == any_(DeliveryPartner.servicable_zipcodes)))).all()

    async def assign_delivery_partner(self, zipcode:int):
        eligible_partners = await self.get_partners_by_zipcode(zipcode=zipcode)

        for partner in eligible_partners:
            if partner.shipments.current_handling_capacity >0:
                return partner

        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No delivery partner available")

        


