# from sqlmodel import SQLModel, Field, create_engine, Session
# from contextlib import asynccontextmanager

# class Test(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     name:str


# sqlite_url = "sqlite://database.db"
# engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread":True})

# @asynccontextmanager
# async def lifespan_hanlder(app:FastAPI)
#     SQLModel.metadata,create_all(engine)

# app = FastAPI(lifespan=lifespan_hanlder)

# def get_session():
#     with Session(engine) as session:
#     yield session

# SessionDeps = Annotated[Session, Depends(get_session)]

# @app.get("/")
# def get_one(id:int, db:SessionDeps):
#     db.get()