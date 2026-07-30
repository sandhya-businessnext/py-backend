from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database.session import get_session
from .services.seller import SellerService

from .core.security import oauth2_scheme

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_seller_service(session:SessionDep):
    return SellerService(session)

SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

OAuthDep = Annotated[str, Depends(oauth2_scheme)]