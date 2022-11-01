from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from backend import service
from backend.sql_app import schemas
from backend.sql_app.crud import create_user, create_register_request, login, authenticate_user
from backend.sql_app.database import get_db
from backend.sql_app.schemas import User
from backend.utils.workWithFile import get_flats_from_excel_file, save_file, update_file, get_file

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
    await save_file(file, 'flats/' + file.filename)
    return flats, file.filename


@userRouter.get("/getAnalogs")
async def get_analogs(flat: schemas.Flat):
    analogs = service.find_analogs(flat)
    return analogs


@userRouter.get("/calculateCost")
async def calculate_cost(flats: list[schemas.Flat]):
    analogs = service.calculate_cost(flats)
    return analogs


@userRouter.get("/downloadFile")
async def download_file(flats_prices: list[float], filename: str):
    await update_file(flats_prices, filename)
    file = await get_file(filename)
    return file
