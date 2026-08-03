from datetime import datetime
from enum import Enum

from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import ARRAY, INTEGER, Column, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, Relationship, SQLModel


class ShipmentStatus(str,Enum):
    PLACED = "Placed"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    PENDING = "Pending"
    CANCELLED = "Cancelled"

class Shipment(SQLModel, table=True): # table True is used to indicate that this model should be used to create a table, else it is just a regular model like pydantic models
    __tablename__ = "shipments_table"
    id:UUID = Field(sa_column=Column(
           postgresql.UUID(as_uuid=True),
             primary_key=True, default=uuid4
        ))
    content: str
    weight: float = Field(ge=0,le=25)
    destination: int

    address: str | None
    zip_code: str | None

    estimated_delivery: datetime
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )

    timeline:"ShipmentEvent" = Relationship(back_populates="shipment",
                                            sa_relationship_kwargs={"lazy":"selectin"})

    seller_id: UUID = Field(foreign_key="seller_table.id")
    seller: "Seller" = Relationship(back_populates="shipments")
    delivery_partner_id: UUID | None = Field(sa_column=Column(
        postgresql.UUID(as_uuid=True), ForeignKey("delivery_partner.id"), nullable=True))
    delivery_partner:"DeliveryPartner" = Relationship(back_populates="shipments",
                                                      sa_relationship_kwargs={"lazy":"selectin"})

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None 


class ShipmentEvent(SQLModel, table=True):
    __tablename__="shipment_event"
    id:UUID = Field(sa_column=Column(
        postgresql.UUID(as_uuid=True), default=uuid4, primary_key=True
    ))
    created_at:datetime = Field(sa_column=Column(postgresql.TIMESTAMP, default=datetime.now))
    status: ShipmentStatus
    location: str

    description:str | None =  Field(default=None)
    shipment_id: UUID = Field(foreign_key="shipments_table.id")
    shipment:Shipment = Relationship(back_populates="timeline", sa_relationship_kwargs={"lazy":"selectin"})



class User(SQLModel):
    name: str
    email: EmailStr
    password_hash:str


class Seller(User, table=True):
    __tablename__= "seller_table"
    id:UUID = Field(sa_column=Column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4
    ))
    created_at: datetime = Field(
            sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now
            )
        )
    shipments: list[Shipment] = Relationship(back_populates="seller",
                                             sa_relationship_kwargs={"lazy":"selectin"})
    zip_code: int
    address: str | None = Field(default=None)
    zip_code: int | None = Field(default=None)



class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True), default=uuid4, primary_key=True
        )
    )
    created_at: datetime = Field(
            sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now
            )
        )
    servicable_zipcodes: list[int] = Field(
        sa_column=Column(
            ARRAY(INTEGER)
        )
    )
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

    @property
    def active_shipments(self) -> list[Shipment]:
        return [shipment for shipment in self.shipments if shipment.status != ShipmentStatus.DELIVERED or shipment.status != ShipmentStatus.CANCELLED]

    @property
    def current_handling_capacity(self)-> int:
        return self.max_handling_capacity - len(self.active_shipments)
