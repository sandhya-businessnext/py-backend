from app.database.models import Shipment, ShipmentEvent, ShipmentStatus

from ..services.base import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent,session)
        self.session = session

    async def add(self, shipment:Shipment, location:str = None, status:ShipmentStatus = None, description:str = None) -> ShipmentEvent:

        if not location or not status:
            latest_event = await self.get_latest_event(shipment=shipment)
            location = location if location else latest_event.location
            status = status if status else latest_event.status

        new_event = ShipmentEvent(location=location, 
                                  status=status, 
                                  description=description if description else self._generate_description(status=status, location=location),
                                  shipment_id=shipment.id)

        return await self._add(new_event)
    
    async def get_latest_event(self, shipment:Shipment):
        return await sorted(shipment.timeline, key=lambda item: item["created_at"])[-1]

    def _generate_description(self, status:ShipmentStatus, location:str) -> str:
        match status:
            case ShipmentStatus.PLACED:
                return "Shipment has been placed and is awaiting pickup."
            case ShipmentStatus.IN_TRANSIT:
                return "Shipment is currently in transit and on its way to the destination."
            case ShipmentStatus.DELIVERED:
                return "Shipment has been successfully delivered to the recipient."
            case ShipmentStatus.PENDING:
                return "Shipment is pending and awaiting further action."
            case _:
                return f"Shipment has been scanned at {location}."    