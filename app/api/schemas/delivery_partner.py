from pydantic import BaseModel, EmailStr


class BasePartner(BaseModel):
    name:str
    email:EmailStr

class PartnerCreate(BasePartner):
    password:str

class PartnerRead(BasePartner):
    pass