from pydantic import BaseModel, Field
from typing import Literal


class Shipment(BaseModel):
    content:str = Field(max_length=100)
    weight:float  = Field(le=25, ge=0, default=0)
    status:Literal["Placed" ,"In Transit" , "Delivered" , "Pending"] = Field(default="Placed")