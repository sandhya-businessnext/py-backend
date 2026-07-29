from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from ..schemas.shipment_schema import ShipmentRead, ShipmentCreate
from ...database.session import SessionDep
from ...database.models import Shipment


router = APIRouter()


@router.get("/shipments",response_model=list[ShipmentRead])
async def get_all_shipments(session:SessionDep):
    return await session.get_all(Shipment)

@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id:int, session:SessionDep):
    shipment = await session.get(Shipment, ident=id)
    if shipment is not None:
        return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    
    

@router.post("/shipment", response_model=ShipmentRead|None)
async def add_shipment(shipment:ShipmentCreate, session:SessionDep):
    new_id = session.add(Shipment())
    await session.commit()
    await session.refresh(shipment)
    return new_id


@router.put("/shipment")
async def update_shipment(id:int, shipment:ShipmentRead, db:SessionDep):
   try:
     shipment = db.update(id, shipment)
     await db.commit()
     await db.refresh(shipment)
    
     return {"detail":"Shipment updated successfully", "shipment":shipment}
   except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

# @router.patch("/shipment")
# def patch_shipment(id:int, shipment:ShipmentUpdate):
#     if id not in shipments:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
#     updates = shipment.model_dump(exclude_none=True)
#     if "status" in updates:
#         updates["status"] = updates["status"].value
#     shipments[id].update(updates)
#     return {"detail": "Shipment updated successfully", "shipment": shipments[id]}

@router.delete("/shipment")
async def delete_shipment(id:int, db:SessionDep):
    if not await db.delete(id):
        raise HTTPException(sttaus_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return {"detail": f"Shipment #{id} deleted"}