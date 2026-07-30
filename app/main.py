from contextlib import asynccontextmanager
from sqlite3 import Error as SQLiteError

import uvicorn
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .api.router import master_router as router
from .database.session import create_db_tables


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print("Server Starting up...")
    await create_db_tables()
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


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)