from uuid import UUID

from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus


class BaseShipment(BaseModel):
    id:UUID | None
    content:str = Field(max_length=100)
    weight:float  = Field(le=25, ge=0, default=0)
    status:ShipmentStatus = ShipmentStatus.PLACED

class ShipmentRead(BaseShipment):
    pass

class ShipmentCreate(BaseShipment):
    id:None = None

class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None, max_length=100)
    weight: float | None = Field(default=None, le=25, ge=0)
    status: ShipmentStatus | None = None