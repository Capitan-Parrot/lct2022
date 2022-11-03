from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from backend import service
from backend.sql_app import schemas
from backend.sql_app.crud import create_user, create_register_request, authenticate_user
from backend.sql_app.database import get_db
from backend.sql_app.schemas import User
from backend.utils.workWithFile import get_flats_from_excel_file, save_file, update_file

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
async def create_upload_file(file: UploadFile, user: User):
    flats = await get_flats_from_excel_file(file)
    await save_file(file, f'flats/{user.name}/{file.filename}')
    return flats


@userRouter.get("/getAnalogs")
async def get_analogs(base_flat: schemas.Flat):
    analogs = service.find_analogs(base_flat)
    return analogs


@userRouter.get("/calculateCost")
async def calculate_cost(flats: list[schemas.Flat], base_flats: dict[int, schemas.Flat]):
    flats = service.calculate_cost(flats, base_flats)
    return flats


@userRouter.post("/downloadFile")
async def download_file(flat_request: schemas.FlatRequest):
    await update_file(flat_request)
    return FileResponse('files/' + flat_request.filename)
