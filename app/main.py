from fastapi import FastAPI, status, HTTPException
from pydantic import ValidationError
from typing import Any
from scalar_fastapi import get_scalar_api_reference
from .schemas import Shipment

app = FastAPI()

shipments = {
    1: {"id": 1, "content": "Laptop", "weight": 2.5, "status": "In Transit"},
    2: {"id": 2, "content": "Phone", "weight": 0.4, "status": "Delivered"},
    3: {"id": 3, "content": "Tablet", "weight": 0.8, "status": "Pending"},
    4: {"id": 4, "content": "Headphones", "weight": 0.3, "status": "In Transit"},
}




@app.get("/shipment")
def get_shipment(id:int) -> dict[str,Any]:
    if id in shipments:
        return shipments[id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    
    

@app.post("/shipment")
def add_shipment(weight:float, data:dict[str, Any]):
    if weight > 25:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Maximum limit is 25kgs")
    
    new_id = max(shipments.keys()) + 1
    content = data["content"]
    shipments[new_id] = {
        "content":content,
        "weight":weight,
        "status":"Placed"
    }
    return shipments[new_id]

@app.get("/shipment/{field}")
def get_shipment_field(field:str, id:int) -> Any:
    return shipments[id][field]

@app.put("/shipment")
def update_shipment(id:int, shipment:Shipment):
   try:
     shipments[id] = {
        "id":id,
        "content":shipment.content,
        "weight": shipment.weight,
        "status":shipment.status
    }
     return {"detail":"Shipment updated successfully", "shipment":shipments[id]}
   except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@app.patch("/shipment")
def patch_shipment(id:int, data:dict[str, Any]):
    shipments[id].update(data)

@app.delete("/shipment")
def delete_shipment(id:int):
    shipments[id].pop(str(id))
    return f"Shipment with id #{id} deleted"

@app.get("/scalar-docs",include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")