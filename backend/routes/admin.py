from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..sql_app import crud, models, schemas
from ..sql_app.database import get_db
from ..sql_app import schemas

adminRouter = APIRouter(prefix="/admin")


@adminRouter.get("/")
async def root():
    return {"message": "Hello Admin Api"}


@adminRouter.get("/getAllUsers", response_model=list[schemas.User])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@adminRouter.get("/getAllRegisterRequests", response_model=list[schemas.RegisterRequest])
async def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_register_requests(db, skip=skip, limit=limit)
    return users


@adminRouter.post("/register")
async def register(register_request_id: schemas.RegisterUser, db: Session = Depends(get_db)):
    user = crud.get_register_request(db, register_request_id.id)
    user, user_password = crud.create_user(db, user)
    return user, user_password

