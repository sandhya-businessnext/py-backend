from typing import Annotated

from fastapi import Depends

from app.services.seller import SellerService

from ..database.session import SessionDep

def get_seller_service(session:SessionDep):
    return SellerService(session=session)


SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]