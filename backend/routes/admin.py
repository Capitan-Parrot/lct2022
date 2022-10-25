from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.sql_app import crud, models, schemas
from backend.sql_app.database import get_db
from backend.sql_app import schemas

adminRouter = APIRouter(prefix="/admin")


@adminRouter.get("/getAllUsers", response_model=list[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@adminRouter.get("/")
async def root():
    return {"message": "Hello Admin Api"}