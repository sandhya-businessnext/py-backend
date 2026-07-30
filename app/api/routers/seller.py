from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.utils import verify_access_token
from app.database.models import Seller

from ...dependencies import OAuthDep, SellerServiceDep

from ..schemas.seller import SellerCreate, SellerRead

router  = APIRouter(prefix="/seller", tags=["Seller"])

@router.post("/signup", response_model=SellerRead)
async def register_seller(seller:SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/login")
async def get_token(service:SellerServiceDep, request_form:Annotated[OAuth2PasswordRequestForm, Depends()]):
   token =  await service.token(request_form.username, request_form.password)
   return {"message":"Login successful", "token":token}
    
@router.post("/dashboard")
async def get_dashboard(token:OAuthDep, service:SellerServiceDep) -> SellerRead:
    data =  verify_access_token(token)
    print(data)
    return await service.session.get(Seller,data["user"]["id"])


