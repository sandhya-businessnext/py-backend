from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment_schema import ShipmentCreate
from app.database.models import Seller, Shipment, ShipmentStatus
from app.services import delivery_partner

from ..services.base import BaseService


class ShipmentService(BaseService):
    def __init__(self, session:AsyncSession, partner_service:delivery_partner.DeliveryPartnerService):
        super().__init__(model=Shipment, session=session)
        self.partner_service = partner_service
    # Get a shipment by id
        async def get(self, id: UUID) -> Shipment | None:
            return await self._get(id)

    async def add(self, shipment_create:ShipmentCreate, seller:Seller):
        new_shipment = Shipment(**shipment_create.model_dump(),
                               estimated_delivery=datetime.now() + datetime.timedelta(days=3),
                               seller_id=seller.id,
                               status=ShipmentStatus.PLACED

                               )
         # Assign delivery partner to the shipment
        partner = await self.partner_service.assign_shipment(
                    new_shipment,
                )
                # Add the delivery partner foreign key
        new_shipment.delivery_partner_id = partner.id
        return await self._add(new_shipment)

    # Update an existing shipment
    async def update(self, shipment: Shipment) -> Shipment:
        return await self._update(shipment)
    
    # Delete a shipment
    async def delete(self, id: int) -> None:
        await self._delete(await self.get(id))

