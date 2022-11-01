from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from backend import service
from backend.dependencies import get_flats_from_excel_file
from backend.sql_app import schemas
from backend.sql_app.crud import create_user, create_register_request, login, authenticate_user
from backend.sql_app.database import get_db
from backend.sql_app.schemas import User

userRouter = APIRouter(prefix="/user")


@userRouter.post("/register")
async def register(register_request: schemas.RegisterUserRequest, db: Session = Depends(get_db)):
    request_status = create_register_request(db, register_request)
    return request_status


@userRouter.post("/login", response_model=User)
async def login(login_request: schemas.LoginUserRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_request)
    return user


@userRouter.post("/uploadFile")
async def create_upload_file(file: UploadFile):
    flats = await get_flats_from_excel_file(file)
    return flats


@userRouter.get("/getAnalogs")
async def get_analogs(flat):
    analogs = service.find_analogs(flat)
    return analogs


@userRouter.get("/calculateCost")
async def calculate_cost(flats):
    analogs = service.calculate_cost(flats)
    return analogs


@userRouter.get("/downloadFile")
async def download_file(flats):
    flats = service.create_file(flats)
    service.save_file(flats)
    return flats
