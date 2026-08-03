from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.delivery_partner import DeliveryPartnerService
from app.services.shipment import ShipmentService
from app.services.shipment_event import ShipmentEventService

from .database.session import get_session
from .services.seller import SellerService

from .core.security import oauth2_scheme

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_seller_service(session:SessionDep):
    return SellerService(session)

def get_delivery_partner_service(session:SessionDep):
    return DeliveryPartnerService(session)

def get_shipment_service(session:SessionDep, partner_service:DeliveryPartnerService, event_service:ShipmentEventService):
    return ShipmentService(session=session, partner_service=partner_service, event_service=event_service)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
DeliveryPartnerServiceDep = Annotated[DeliveryPartnerService, Depends(get_delivery_partner_service)]
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

OAuthDep = Annotated[str, Depends(oauth2_scheme)]