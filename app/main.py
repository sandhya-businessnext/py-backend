from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import ValidationError
from scalar_fastapi import get_scalar_api_reference
from .schemas import ShipmentRead, ShipmentCreate
from sqlite3 import Error as SQLiteError
from contextlib import asynccontextmanager
from app.database.models import create_db_tables, Shipment
from app.database.session import SessionDep

@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print("Server Starting up...")
    create_db_tables()
    yield
    print("...Server shutting down")


app = FastAPI(lifespan=lifespan_handler)

# db =  Database()




@app.get("/shipments",response_model=list[ShipmentRead])
def get_all_shipments(session:SessionDep):
    return session.get_all(Shipment)

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id:int, session:SessionDep):
    shipment = session.get(Shipment, ident=id)
    if shipment is not None:
        return shipment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    
    

@app.post("/shipment", response_model=ShipmentRead|None)
def add_shipment(shipment:ShipmentCreate, session:SessionDep):
    new_id = session.add(Shipment())
    return new_id


@app.put("/shipment")
def update_shipment(id:int, shipment:ShipmentRead, db:SessionDep):
   try:
     shipment = db.update(id, shipment)
    
     return {"detail":"Shipment updated successfully", "shipment":shipment}
   except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

# @app.patch("/shipment")
# def patch_shipment(id:int, shipment:ShipmentUpdate):
#     if id not in shipments:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
#     updates = shipment.model_dump(exclude_none=True)
#     if "status" in updates:
#         updates["status"] = updates["status"].value
#     shipments[id].update(updates)
#     return {"detail": "Shipment updated successfully", "shipment": shipments[id]}

@app.delete("/shipment")
def delete_shipment(id:int, db:SessionDep):
    if not db.delete(id):
        raise HTTPException(sttaus_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return {"detail": f"Shipment #{id} deleted"}
@app.get("/scalar-docs",include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")

@app.exception_handler(SQLiteError)
def sqlite_exception_handler(request, exc):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))