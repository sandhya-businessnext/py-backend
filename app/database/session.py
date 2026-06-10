from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from typing import Annotated
from fastapi import Depends


engine = create_engine(url='sqlite:///shipments.db', echo=True)

from .models import Shipment
def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
     yield session

SessionDep = Annotated[Session, Depends(get_session)]