from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from datetime import datetime
from pydantic import EmailStr
from uuid import uuid4, UUID

class ShipmentStatus(Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    PENDING = "Pending"


class Shipment(SQLModel, table=True): # table True is used to indicate that this model should be used to create a table, else it is just a regular model like pydantic models
    __tablename__ = "shipments_table"
    id:UUID = Field(sa_column=Column(
            postgresql.UUID, primary_key=True, default=uuid4
        ))
    content: str
    weight: float = Field(ge=0,le=25)
    status: ShipmentStatus
    estimated_delivery: datetime
    seller_id: str = Field(foreign_key="seller_table.id")
    seller: "Seller" = Relationship(back_populates="shipments")


class Seller(SQLModel, table=True):
    __tablename__= "seller_table"
    id:UUID = Field(sa_column=Column(
        postgresql.UUID, primary_key=True, default=uuid4
    ))
    name: str
    email: EmailStr
    password_hash:str
    shipments: list[Shipment] = Relationship(back_populates="seller",
                                             sa_relationship_kwargs={"lazy":"selectin"})
