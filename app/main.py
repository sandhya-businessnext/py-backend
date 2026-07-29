from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import ValidationError
from scalar_fastapi import get_scalar_api_reference

from app.api import master_router as router
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

app.router.include_router(router)


@app.get("/scalar-docs",include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")

@app.exception_handler(SQLiteError)
def sqlite_exception_handler(request, exc):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))