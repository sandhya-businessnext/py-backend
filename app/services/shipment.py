from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment_schema import ShipmentCreate, ShipmentUpdate
from app.database.models import DeliveryPartner, Seller, Shipment, ShipmentStatus
from ..services.delivery_partner import DeliveryPartnerService
from ..services.shipment_event import ShipmentEventService

from ..services.base import BaseService


class ShipmentService(BaseService):
    def __init__(self, session:AsyncSession, 
                 partner_service:DeliveryPartnerService,
                 event_service: ShipmentEventService
                 ):
        super().__init__(model=Shipment, session=session)
        self.partner_service = partner_service
        self.event_service = event_service
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

        shipment = await self._add(new_shipment)
        # Add initial shipment event
        await self.event_service.add(
            shipment=shipment,
            location=seller.zip_code,
            status=ShipmentStatus.PLACED,
            description=f"assigned to {partner.name}"
        )
        return shipment

    # Update an existing shipment
    async def update(self, shipment_id:UUID, shipment_update: ShipmentUpdate, partner:DeliveryPartner) -> Shipment:
           # Update data with given fields
        shipment = await self.get(shipment_id)
        if shipment is None or shipment.partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized to update this shipment",
            )
        update = shipment_update.model_dump(exclude_none=True)
        
        if not update:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No data provided to update",
            )

        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        if len(update) > 1 or not update.estimated_delivery:
            await self.event_service._add(shipment=shipment, **update)

        
        return await self._update()
    
    async def cancel(self, shipment_id:UUID, seller: Seller) -> Shipment:
        shipment = await self._get(shipment_id)

        if shipment.seller_id != seller.id:
            raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised access")
        if shipment.status == ShipmentStatus.DELIVERED:
            raise HTTPException(status=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Delivered shipment cannot be cancelled")

        await self.event_service.add(shipment=shipment, status= ShipmentStatus.CANCELLED)

    
    # Delete a shipment
    async def delete(self, id: int) -> None:
        await self._delete(await self.get(id))

