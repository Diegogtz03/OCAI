from fastapi import FastAPI
# from .routers import users
from database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(users.router)

@app.get("/")
async def read_root():
  return {"Hello": "World"}