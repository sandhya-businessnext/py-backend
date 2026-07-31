from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.delivery_partner import DeliveryPartnerService

from .database.session import get_session
from .services.seller import SellerService

from .core.security import oauth2_scheme

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_seller_service(session:SessionDep):
    return SellerService(session)

def get_delivery_partner_service(session:SessionDep):
    return DeliveryPartnerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
DeliveryPartnerServiceDep = Annotated[DeliveryPartnerService, Depends(get_delivery_partner_service)]

OAuthDep = Annotated[str, Depends(oauth2_scheme)]