from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class ShipmentStatus(Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    PENDING = "Pending"


class Shipment(SQLModel, table=True): # table True is used to indicate that this model should be used to create a table, else it is just a regular model like pydantic models
    __tablename__ = "shipments_table"
    id: str = Field(primary_key=True)
    content: str
    weight: float = Field(ge=0,le=25)
    status: ShipmentStatus
    estimated_delivery: datetime
 

