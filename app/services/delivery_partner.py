
from sqlalchemy.ext.asyncio import AsyncSession

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

    

        


