from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...api.schemas.delivery_partner import PartnerCreate, PartnerRead
from app.core.utils import verify_access_token
from app.database.models import DeliveryPartner

from ...dependencies import DeliveryPartnerServiceDep, OAuthDep, SellerServiceDep


router  = APIRouter(prefix="/delivery_partner", tags=["Delivery Partner"])

@router.post("/signup", response_model=PartnerRead)
async def register_partner(partner:PartnerCreate, service: DeliveryPartnerServiceDep):
    return await service.add(partner)


@router.post("/login")
async def get_token(service:DeliveryPartnerServiceDep, request_form:Annotated[OAuth2PasswordRequestForm, Depends()]):
   token =  await service.token(request_form.username, request_form.password)
   return {"message":"Login successful", "token":token}
    
@router.post("/dashboard")
async def get_dashboard(token:OAuthDep, service:SellerServiceDep) -> PartnerRead:
    data =  verify_access_token(token)
    print(data)
    return await service.session.get(DeliveryPartner,data["user"]["id"])


